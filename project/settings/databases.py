from .environment import BASE_DIR

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'RecipeBook',  
        'USER': 'root',   
        'PASSWORD': '2270',
        'HOST': 'localhost',
        'PORT': '3306', 
    }
}
