from decouple import config
NAMEBD=config('NAME')
USERDB=config('USER')
PASSWORDDB=config('PASSWORD')
HOSTBD=config('HOST')


MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': NAMEBD,
        'USER': USERDB,
        'PASSWORD': PASSWORDDB,
        'HOST': HOSTBD,
        'PORT': '3306',  # Puedes establecer un valor por defecto
    }
}


