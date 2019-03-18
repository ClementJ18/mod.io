from distutils.core import setup

setup(name='modio',
      version='0.2.0',
      description='mod.io python wrapper',
      author='Clement Julia',
      author_email='clement.julia13@gmail.com',
      url='https://github.com/ClementJ18/mod.io',
      packages=['modio'],
      install_requires=[
        'requests>=2.20.0'
      ]
     )

setup(name='async_modio',
      version='0.2.0',
      description='async mod.io python wrapper',
      author='Clement Julia',
      author_email='clement.julia13@gmail.com',
      url='https://github.com/ClementJ18/mod.io',
      packages=['async_modio'],
      install_requires=[
        'aiohttp==3.4.4'
      ]
     )