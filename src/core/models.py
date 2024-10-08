from django.db import models, transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import qrcode
import os
from io import BytesIO
from django.core.files import File
from django.conf import settings
from django.core.exceptions import ValidationError


class SequentialTag(models.Model): 
    """
    Modelo SequentialTag, el cual se usará para generar el tag de cada instrumento.
    """
    prefix = models.CharField(max_length=3, unique=True)
    latest = models.IntegerField(default=0) 

def __str__(self):
        return f"{self.prefix}-{self.latest}"

  
class Tag(models.Model):
    """
    Modelo en donde su ID está definido como la concatenación de prefix y latest
    del modelo SequentialTag (no es autoincremental).
    """
    OPTIONS_MAGNITUDE = [ #Opciones para las magnitudes
        ('P', 'PRESION'),
        ('T', 'TEMPERATURA'),
        ('N', 'NIVEL'),
        ('F', 'FLUJO'),
        ('V', 'VIBRACIONES'),
    ]
    
    OPTIONS_TECHNOLOGY = [ #Opciones para las tecnologías
        ('T', 'TRANSMISOR'),
        ('S', 'SWITCH'),
        ('X', 'SIN TECNOLOGIA')
    ]
    
    OPTIONS_DISPLAY = [ #Opciones para el display
        ('I', 'CON INDICACION'),
        ('X', 'SIN INDICACION'),
        ('A', 'ABSOLUTAS'),
        ('R', 'RELATIVAS'),
        ('P', 'PATRON'),
    ]
    
    id = models.CharField(primary_key=True, max_length=7) 
    magnitude = models.CharField(max_length=1, choices=OPTIONS_MAGNITUDE, editable=True)
    technology = models.CharField(max_length=1, choices=OPTIONS_TECHNOLOGY, editable=True)
    display = models.CharField(max_length=1, choices=OPTIONS_DISPLAY, editable=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    @classmethod
    def create_prefix (cls, magnitude, technology, display):
        """
        Creo el prefijo utilizando estos 3 argumentos concatenados.
        """
        return f"{magnitude}{technology}{display}"

    @classmethod
    def create_with_sequential_id(cls, magnitude, technology, display, description):
        """
        El modelo de Sequential_id, utiliza una transaccion atomica para asegurar que todas las operaciones
        de base de datos dentro de este bloque de código se ejecuten solo si se completan todas las acciones.
        
        Se pone el save() dentro de la transacción, para que pueda ser revertido si no se realiza el commit al
        final de la transacción.
        """
        with transaction.atomic():
        
            prefix = cls.create_prefix(magnitude, technology, display)
            seq_tag, created = SequentialTag.objects.get_or_create(prefix=prefix)
            seq_tag.latest += 1
            seq_tag.save()
            new_id = f"{prefix}-{seq_tag.latest:03d}"
            return cls.objects.create(
                id=new_id,
                magnitude=magnitude,
                technology=technology,
                display=display,
                description=description
            )

    def save(self, *args, **kwargs):
        """
        Define dentro del save la generacion del codigo QR en base al tag_id.
        """
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.id)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            filename = f'{self.id}.png'
            self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)

        
class Location(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    

class Attachment(models.Model):
    """
    Modelo para crear una tabla de adjuntos con un atributo de claves genericas,
    el cual se usa para indexar a cada tabla que lleve adjuntos.

    Guarda una referencia al tipo de contenido (modelo) al que está asociado este adjunto.
    """
    table = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    table_instance = models.PositiveIntegerField()
    content_object = GenericForeignKey('table', 'table_instance')
    media_path = models.FileField(upload_to='attachments/')
    name = models.CharField(max_length=50, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)

 
class Instrument(models.Model):
    tag = models.OneToOneField(Tag, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.RESTRICT)
    location_comments = models.CharField(blank=True, null=True, max_length=50)
    brand = models.CharField(blank=True, null=True, max_length=50)
    model = models.CharField(blank=True, null=True, max_length=50)
    range = models.CharField(blank=True, null=True, max_length=20)
    unit = models.CharField(blank=True, null=True, max_length=10)
    process_connection = models.CharField(blank=True, null=True, max_length=20)
    serial_number = models.CharField (blank=True, null=True, max_length=20)
    traceable = models.BooleanField(default=False)
    removal_date = models.DateTimeField(blank=True, null=True)
    removal_reason = models.CharField(blank=True, null=True, max_length=100)
    attachments = GenericRelation(Attachment, object_id_field='table_instance', content_type_field='table')

    def __str__(self):
        return f'{self.tag}'
    
    def get_related_data(self):
        """
        Devuelve todas las instancias de Check, Contrast, y SetUp relacionadas con este instrumento,
        junto con los archivos adjuntos, si los tienen.
        """
        related_data = {
            'checks': [],
            'contrasts': [],
            'setups': []
        }
        
        # Recuperar instancias de Check
        checks = Check.objects.filter(instrument=self)
        for check in checks:
            attachments = Attachment.objects.filter(content_object=check)
            related_data['checks'].append({'instance': check, 'attachments': attachments})
        
        # Recuperar instancias de Contrast
        contrasts = Contrast.objects.filter(instrument=self)
        for contrast in contrasts:
            attachments = Attachment.objects.filter(content_object=contrast)
            related_data['contrasts'].append({'instance': contrast, 'attachments': attachments})
        
        # Recuperar instancias de SetUp
        setups = SetUp.objects.filter(instrument=self)
        for setup in setups:
            attachments = Attachment.objects.filter(content_object=setup)
            related_data['setups'].append({'instance': setup, 'attachments': attachments})
            
        # Obtener el último 'SetUp' donde 'alarm_set' no sea None
        latest_alarm_setup = setups.filter(alarm_set__isnull=False).order_by('-date').first()
        
        # Obtener el último 'SetUp' donde 'trip_set' no sea None
        latest_trip_setup = setups.filter(trip_set__isnull=False).order_by('-date').first()
        
        # Añadir los resultados al diccionario de datos relacionados
        related_data['latest_alarm_setup'] = latest_alarm_setup
        related_data['latest_trip_setup'] = latest_trip_setup
        
        return related_data
    

class SetUp(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='setups')
    date = models.DateTimeField() #auto_now_add=True)
    gdc_type = models.CharField(max_length=50)
    gdc_number = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    alarm_set = models.FloatField(blank=True, null=True)
    trip_set = models.FloatField(blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True, null=True)
    attachments = GenericRelation(Attachment, object_id_field='table_instance', content_type_field='table')

    def __str__(self):
        return f'{self.date}'
    
    def clean(self):
        # Validar que al menos uno de los campos 'alarm_set' o 'trip_set' no sea None
        if self.alarm_set is None and self.trip_set is None:
            raise ValidationError('Al menos uno de los campos "alarm_set" o "trip_set" debe tener un valor.')
    
    def save(self, *args, **kwargs):
        # Llamar al método clean antes de guardar
        self.clean()
        super().save(*args, **kwargs)


class Check (models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='checks')
    date = models.DateTimeField(auto_now_add=True)
    OPTIONS_RESULT = [
        ('O', 'OK'),
        ('N', 'NO OK'),
        ('R', 'OBSERVADO'),
    ]
    result = models.CharField(choices=OPTIONS_RESULT, max_length=1)
    author = models.CharField(max_length=50)
    comments = models.CharField(max_length=100)
    attachments = GenericRelation(Attachment, object_id_field='table_instance', content_type_field='table')

    def __str__(self):
        return f'{self.date}'


class PatternInstrument (models.Model):
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE)
    calibration_date = models.DateField()
    calibration_lab = models.CharField(max_length=20)
    calibration_number = models.CharField(max_length=20)
    comments = models.CharField(max_length=100, blank=True, null=True)
    attachments = GenericRelation(Attachment, object_id_field='table_instance', content_type_field='table')
    
    def __str__(self):
        return f'{self.instrument}'


class Contrast (models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='contrasts')
    date = models.DateTimeField(auto_now_add=True)
    OPTIONS_RESULT = [
        ('O', 'OK'),
        ('N', 'NO OK'),
        ('R', 'OBSERVADO'),
    ]
    result = models.CharField(choices=OPTIONS_RESULT, max_length=1)
    author = models.CharField(max_length=50)
    expiration = models.DateField()
    p_instrument = models.ForeignKey(PatternInstrument, on_delete=models.RESTRICT)
    comments = models.CharField(max_length=100, blank=True, null=True)
    attachments = GenericRelation(Attachment, object_id_field='table_instance', content_type_field='table')

    def __str__(self):
        return f'{self.date}'


class Meta:
    """
    Se crea un índice en los campos table y table_id para mejorar  el rendimiento de las consultas
    que utilicen estos campos para buscar adjuntos.
    """
    indexes = [
        models.Index(fields=['table', 'table_instance']),
    ]

def __str__(self):
    return self.table.name