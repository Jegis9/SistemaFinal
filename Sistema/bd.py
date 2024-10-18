from decouple import config

MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST'),
        'PORT': config('PORT', default='3306'),  # Puedes establecer un valor por defecto
    }
}


# MYSQL = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'estaciondatabasebmt',
#         'USER': 'aestacionbd',
#         'PASSWORD': 'baseD3d4t0sE27ac10n',
#         'HOST': 'databaseestacion.c32004mmq5g8.us-east-2.rds.amazonaws.com',
#         'PORT': '3306',
#     }
# }


