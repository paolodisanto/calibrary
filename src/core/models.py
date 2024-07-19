from django.db import models, transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey    

#Generación del modelo SequentialTag, el cual se usará para generar el tag de cada instrumento
class SequentialTag(models.Model): 
    prefix = models.CharField(max_length=3, unique=True)
    latest = models.IntegerField(default=0) 

def __str__(self):
        return f"{self.prefix}-{self.latest}"

#Generación del modelo Tag, en donde su ID está definido como la concatenación de prefix y latest de la tabla anterior (no es autoincremental)    
class Tag(models.Model):
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
    
    id = models.CharField(primary_key=True, max_length=7) #Se establace id como key de tipo charfield, con un maximo de 7 caracteres. Esto se hace para estandarizar el mismo
    magnitude = models.CharField(max_length=1, choices=OPTIONS_MAGNITUDE, editable=True)
    technology = models.CharField(max_length=1, choices=OPTIONS_TECHNOLOGY, editable=True)
    display = models.CharField(max_length=1, choices=OPTIONS_DISPLAY, editable=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    @classmethod #Creamos el prefijo "prefix" con "magnitude", "technology" y "display"
    def create_prefix (cls, magnitude, technology, display):
        return f"{magnitude}{technology}{display}"

    @classmethod #Convierte el método en un método de clase en Python
    def create_with_sequential_id(cls, magnitude, technology, display, description):
 
        with transaction.atomic():
        #Se usa para asegurar que todas las operaciones de base de datos dentro de este bloque de código se ejecuten en una única transacción atómica (si no se completan todas no se realiza)           
       
            prefix = cls.create_prefix(magnitude, technology, display)
            seq_tag, created = SequentialTag.objects.get_or_create(prefix=prefix) #Obtiene o crea un objeto SequentialTag con el prefijo especificado.
            seq_tag.latest += 1 #Incrementa el contador latest en 1 y guarda los cambios.
            seq_tag.save() #Al estar el save() dentro de la transacción, puede ser revertido si no se realiza el commit al final de la transacción
            new_id = f"{prefix}-{seq_tag.latest:03d}"  #Se ajusta el formato para que muestre 3 dígitos enteros con ceros antes para rellenar.
            return cls.objects.create(
                id=new_id,
                magnitude=magnitude,
                technology=technology,
                display=display,
                description=description
            )

#Generación del modelo Location
class Location(models.Model):
    id = models.CharField(primary_key=True, max_length=3) #Se establece id como key de tipo charfield, con un maximo de 3 caracteres.
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
"""
    #generación del modelo Location2
    class Location2(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
""" 

#Generación del modelo Instrument   
class Instrument(models.Model):
    tag = models.OneToOneField(Tag, on_delete=models.CASCADE) #Con on_delete si se borra un TAG se borra el instrumento asociado
    location = models.ForeignKey(Location, on_delete=models.RESTRICT) #No permito borrar la instancia de localización si hay instrumentos que apunten a ella
    #location2 = models.ForeignKey(Location2)
    location_comments = models.CharField(blank=True, null=True, max_length=50)
    brand = models.CharField(blank=True, null=True, max_length=50)
    model = models.CharField(blank=True, null=True, max_length=50)
    range = models.CharField(blank=True, null=True, max_length=20)
    unit = models.CharField(blank=True, null=True, max_length=10)
    process_connection = models.CharField(blank=True, null=True, max_length=20)
    serial_number = models.CharField (blank=True, null=True, max_length=20)
    traceable = models.BooleanField(default=False) #Por defecto se setea en falso y se permite no definir en el formulario
    removal_date = models.DateTimeField(blank=True, null=True)
    removal_reason = models.CharField(blank=True, null=True, max_length=100)
    
    def __str__(self):
        return f'{self.tag}'

#Generación del modelo SetUp
class SetUp(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    date = models.DateTimeField()#, auto_now_add=True) #Se establece en true para que grabe la fecha de creación en forma automática.
    gdc_type = models.CharField(max_length=50)
    gdc_number = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    alarm_set = models.FloatField(blank=True, null=True)
    trip_set = models.FloatField()
    comments = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.date}'

#Generación del modelo Check    
class Check (models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) #Se establece en true para que grabe la fecha de creación en forma automática.
    OPTIONS_RESULT = [ #Se permiten solo 3 opciones para el resultado
        ('O', 'OK'),
        ('N', 'NO OK'),
        ('R', 'OBSERVADO'),
    ]
    result = models.CharField(choices=OPTIONS_RESULT, max_length=1)
    author = models.CharField(max_length=50)
    comments = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.date}'

#Generación del modelo PatternInstrument
class PatternInstrument (models.Model):
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE) #Relación uno a uno con el modelo Instrument
    calibration_date = models.DateField()
    calibration_lab = models.CharField(max_length=20)
    calibration_number = models.CharField(max_length=20)
    comments = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f'{self.instrument}'

#Generación del modelo Contrast
class Contrast (models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) #Se establece en true para que grabe la fecha de creación en forma automática.
    OPTIONS_RESULT = [ #Se permiten solo 3 opciones para el resultado
        ('O', 'OK'),
        ('N', 'NO OK'),
        ('R', 'OBSERVADO'),
    ]
    result = models.CharField(choices=OPTIONS_RESULT, max_length=1)
    author = models.CharField(max_length=50)
    expiration = models.DateField()
    p_instrument = models.OneToOneField (PatternInstrument, on_delete=models.RESTRICT)
    comments = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f'{self.date}'

#Modelo para crear una tabla de adjuntos con un atributo de claves genericas, el cual se usa para indexar a cada tabla que lleve adjuntos
#Generación del modelo Attachment
class Attachment (models.Model):
    table = models.ForeignKey(ContentType, on_delete=models.CASCADE) #Guarda una referencia al tipo de contenido (modelo) al que está asociado este adjunto
    table_instance = models.PositiveIntegerField() #Guarda el identificador de la instancia específica del modelo al que está asociado el adjunto.
    content_object = GenericForeignKey('table', 'table_instance') #Permite acceder a una instancia del modelo asociado directamente
    media_path = models.FileField(upload_to='attachments/')#Guarda la dirección donde se carga el adjunto
    name = models.CharField (max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    
    class Meta: #Se crea un índice en los campos table y table_id para mejorar el rendimiento de las consultas que utilicen estos campos para buscar adjuntos
        indexes = [
            models.Index(fields=['table', 'table_instance']),
        ]

    def __str__(self):
        return self.table.name
    