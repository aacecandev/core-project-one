# CORE PROJECT ONE

A Data Science project to explore demographics of Barcelona city.

## Table of contents

<!-- TOC depthTo:3 -->

- [Project Task List](#project-task-list)
- [Data Source](#data-source)
- [Data Analysis with Jupyter Lab](#data-analysis-with-jupyter-lab)
- [Fast API](#fast-api)
- [Data Visualization](#data-visualization-with-streamlit)
- [MongoDB](#mongodb)
- [Running this project](#running-this-project)
- [Sentry tasks](#sentry-tasks)
- [Contributing](#contributing)
- [Semantic Release](#semantic-release)
- [Resources](#resources)

<!-- /TOC -->

## Project Task List

- L1: Crear api en fastapi
- L1: Crear dashboard en streamlit
- L1: Base de datos en MongoDB o PostgreSQL
- L2: Utilizar de datos geoespaciales y geoqueries en MongoDB o Postgres (Usando PostGIS)*
- L2: Tener la base de datos en el Cloud (Hay servicios gratis en MongoDB Atlas, Heroku Postgres, dentre otros)
- L2: Generar reporte pdf de los datos visibles en Streamlit, descargable mediante boton.
- L2: Un dashboard de multiples páginas en Streamlit
- L3: Que el dashboard te envie el reporte pdf por e-mail
- L3: Poder subir nuevos datos a la bbdd via la API (usuario y contraseña como headers del request)
- L4: Poder actualizar la base de datos via Streamlit (con usuario y contraseña, en una página a parte. El dashboard  debe hacer la petición anterior que añade datos via API)
- L4: Crear contenedor Docker y hacer deploy de los servicios en el cloud (Heroku. Los dos servicios deben subirse separadamente)
- L5: Controlar el pipeline con Apache Airflow

## Data Source

This project is based on a dataset of [Barcelona city](https://www.datos.gov.es/portal/site/dataset/barcelona-city-demographics-and-population-statistics-2017) that contains information about demographics and population statistics.

For this project, we will using the accidents dataset, which contains useful information about dates, places, and accidents.

## Data Analysis with Jupyter Lab

To make the Exploratory Data Analysis, I've used [Jupyter Lab](https://jupyter.org/)

During the analysis, I've used the following libraries:

- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [seaborn](https://seaborn.pydata.org/)
- [numpy](https://numpy.org/)
- [geopy](https://geopy.readthedocs.io/)
- [requests](https://requests.readthedocs.io/)
- [re](https://docs.python.org/3/library/re.html)
- [threading](https://docs.python.org/3/library/threading.html)
- [pymongo](https://api.mongodb.com/python/current/)

For this stage of the project, the main concern has been to understand the data in order to be able to make interesting questions (and visualizations then) about it.

Furthermore, I've been extremely interested in reducing the dataset weight, which I've achieved passing from a 6MB file to a 240KB file. This has been achieved reducing the number of unnecesary columns, cleaning the data and assigning the correct data type to it.

Another interesting aspect is that requiring location information with the `geopy` API is very limited, so I've investigated about Python multithreading capabilities and implemented parallel requests using high performance methods.

You can run a notebook in the `data` folder and repeat my steps, and when you're done, export the DataFrame to a JSON file that will feed the local MongoDB database, or just upload it with your own URL in an `.env` file.

## Fast API

This projects uses `Fast API` as its backend to create the API.

In this project I've levereaged the following features:

- Asynchronous API
- Asynchronous testing of the main route
- Asynchronous MongoDB queries using `motor`
- Routing with regex
- OpenAPI documentation
- Sentry integration
- Python type hinting with `pydantic`
- Type annotations with `typing`
- Pydantic validation through models
- Docker deployment using `gunicorn` with `ASGI` asynchronous workers

This project's API is deployed in a Docker container and to be able to run it locally, you must have an `.env` file with the following variables:

- DATABASE_URL
- DATABASE_NAME
- DEBUG
- ENVIRONMENT
- SENTRY_DSN

## Data Visualization with Streamlit

To be able to query Fast API I've used Streamlit as a frontend, wrapped with the Hydralit library to get some nice forntend features.

Within the frontend you will be able to make a couple of queries to the API, and you will be able to see the results in a nice dashboard.

The dashboard also implements a few other features, such as a search bar, a map, a table, and a graph.

There's a user panel in which you will be able to interact with the database, and you can also see the documentation of the API.

A user can also upload a new dataset to the database, and the dashboard will be updated with the new data. This is done through the API.

Another cool feature is that you can download a report of the data, which I've achieved using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

## MongoDB

When you export the DataFrame with Jupyter, the data is stored in a folder that contains a MongoDB Dockerfile which will be used to create a MongoDB container automatically.

## Running this project

This projects uses `Makefile`. The following options are available:

- help: Show the help
- build-docker-api: Build the Docker image for the API
- lint-docker-api: Lint the Docker image for the API
- run-docker-api: Run the Docker image for the API
- build-docker-db: Build the Docker image for the MongoDB
- lint-docker-db: Lint the Docker image for the MongoDB
- run-docker-db: Run the Docker image for the MongoDB
- build-docker-streamlit: Build the Docker image for the Streamlit
- lint-docker-streamlit: Lint the Docker image for the Streamlit
- run-docker-streamlit: Run the Docker image for the Streamlit
- run-app: Run the application using docker compose
- rm-app: Remove the docker-compose stack

## Pre-commit

This project uses `pre-commit` to test the repository files before making a commit.

You need to install it with `pip install pre-commit` within the repository

## Sentry

This project uses `Sentry` to send errors to the developers. It is configured with the `SENTRY_DSN` environment variable in Fast API

## Contributing

Pull Requests are welcome! Feel free to contribute to the project.

### Semantic release

This project uses [Semantic Release](https://github.com/semantic-release/semantic-release) and every push to the `main` branch will trigger a workflow that generates a `CHANGELOG.md` file.
## Resources

- pre-commit
    - https://pre-commit.com/index.html
    - https://towardsdatascience.com/pre-commit-hooks-you-must-know-ff247f5feb7e
    - https://github.com/zricethezav/gitleaks
- codecov
    -

- Pandas memory usage
    - https://pythonspeed.com/articles/pandas-load-less-data/

Pandas SettingWithcopyWarning
    - https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-view-versus-copy
    - https://www.dataquest.io/blog/settingwithcopywarning/

https://jira.mongodb.org/browse/MOTOR-822
https://testdriven.io/blog/fastapi-mongo/

https://docs.gunicorn.org/en/stable/configure.html#configuration-file
https://fastapi.tiangolo.com/deployment/docker/#replication-number-of-processes
https://github.com/tiangolo/uvicorn-gunicorn-docker
https://fastapi.tiangolo.com/advanced/async-tests/
https://www.python-httpx.org/advanced/
https://pypi.org/project/asgi-lifespan/

https://medium.com/codex/automated-github-actions-deployment-with-semantic-release-d8f8ae9c6252
https://semantic-release.gitbook.io/semantic-release/extending/plugins-list#community-plugins
https://semantic-release.gitbook.io/semantic-release/extending/plugins-list#official-plugins
https://github.com/juliuscc/semantic-release-slack-bot
https://github.com/pmowrer/semantic-release-monorepo/blob/master/package.json
https://motor.readthedocs.io/en/stable/differences.html
https://testdriven.io/blog/fastapi-mongo/
https://github.com/encode/starlette/blob/master/starlette/status.py
https://docs.python.org/3/library/functools.html#functools.lru_cache
https://betterprogramming.pub/metadata-and-additional-responses-in-fastapi-ea90a321d477
https://stackoverflow.com/questions/41584243/runtimeerror-task-attached-to-a-different-loop
https://deckgl.readthedocs.io/en/latest/gallery/hexagon_layer.html
https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart
https://discuss.streamlit.io/t/creating-a-pdf-file-generator/7613
https://github.com/tiangolo/fastapi/issues/1515
https://www.geeksforgeeks.org/python-functools-lru_cache/
https://www.modelingonlineauctions.com/datasets
https://jeande.medium.com/how-to-do-exploratory-data-analysis-effectively-b530d0e4de
https://medium.com/analytics-vidhya/data-visualization-and-exploratory-data-analysis-eda-in-data-science-984e84942fda
https://towardsdatascience.com/an-extensive-guide-to-exploratory-data-analysis-ddd99a03199e
https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf
https://github.com/abjmorrison/MediumTutorials/blob/main/GeoPyExamples/GeoPy_NominatimExample.py
https://wiki.openstreetmap.org/wiki/Nominatim
https://mappinggis.com/2018/11/geocodificacion-con-geopy/
https://curc.readthedocs.io/en/latest/gateways/parallel-programming-jupyter.html
https://pypi.org/project/multiprocess/
https://stackoverflow.com/questions/16982569/making-multiple-api-calls-in-parallel-using-python-ipython
https://nbviewer.org/gist/minrk/5732094
https://pretagteam.com/question/multiprocessing-vs-threading-in-jupyter-notebook

Streamlit pdf
https://discuss.streamlit.io/t/creating-a-pdf-file-generator/7613/2
https://discuss.streamlit.io/t/deploying-an-app-using-using-wkhtmltopdf-on-herokou/12029/8

Deploy heroku
https://devcenter.heroku.com/articles/container-registry-and-runtime
https://devcenter.heroku.com/articles/build-docker-images-heroku-yml
https://github.com/marketplace/actions/deploy-to-heroku#environment-variables
https://github.com/SFDO-Tooling/Metecho/blob/main/heroku.yml

Dcoument fastapi
https://www.linode.com/docs/guides/documenting-a-fastapi-app-with-openapi/

Streamlit maps
https://discuss.streamlit.io/t/ann-streamlit-folium-a-component-for-rendering-folium-maps/4367

Mypy
https://mypy.readthedocs.io/en/stable/

Uvicorn
https://www.uvicorn.org/settings/

Pydantic
https://pydantic-docs.helpmanual.io/

Codecov
https://github.com/codecov/codecov-action
https://app.codecov.io/gh/aacecandev/core-project-one
https://github.com/codecov/example-python
https://github.com/nedbat/coveragepy
