from setuptools import setup, find_packages

setup(
    name="mysite",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "wagtail>=5.0,<5.1",
        "Django>=4.2,<4.3",
        "psycopg2-binary>=2.9.6",
        "dj-database-url>=2.0.0",
        "python-dotenv>=1.0.0",
        "gunicorn>=21.2.0",
        "whitenoise>=6.5.0",
    ],
    python_requires=">=3.8",
)