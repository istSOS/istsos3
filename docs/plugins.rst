.. _plugins:

Plugin Development
##################

istSOS3 offer a plugin system. With new plugins you are able to extend istSOS3
with new features and functionalities.

There are two types of plugins that you can integrate: **python plugins** and **web
interfaces**.

Python plugins
==============

With istSOS3 Python Plugins you can add new features, or modify existings
actions.

To create a new Python Plugin create your working directory into the istsos3
plugins folder:

..  code-block:: shell

    cd istsos/plugins
    mkdir istsos3_plugin_name
    cd istsos3_plugin_name
    mkdir lib
    touch README.md config.json __init__.py action.py

Configure your plugin by modifying the config.json file:

.. code-block:: json

    {
        "name": "Ping",
        "version": "1.0.0",
        "author": "Foo Bar",
        "author_email": "me@example.com",
        "description": "This is an istSOS3 plugin",
        "license": "GPL3",
        "url": "http://example.com/ping/",
        "img": "http://example.com/ping/logo.png",
        "api": {
            "PING": [
                "istsos3_plugin_name.action", "PingApi"
            ]
        }
    }

Modifiy your Python code (action.py) implementing the Action or
CompositeAction class, the most important part is the *api* attribute.
Here you register the name of the action with whom your plugin is called.

.. code-block:: python3

    import asyncio
    from istsos.entity.rest.response import Response
    from istsos.actions.action import CompositeAction


    class PingApi(CompositeAction):

        @asyncio.coroutine
        def before(self, request):
            json = request.get_json()
            if 'message' in json:
                request['message'] = json['message']
            yield from self.add_plugin("example", "Ping")

        @asyncio.coroutine
        def after(self, request):
            request['response'] = Response(
                json_source=Response.get_template({
                    "message": request["message"]
                })
            )

Web Interfaces
==============

To build a new web component that can be easy be integrated into the
istsos3-admin interface you have to create an npm package library.

Create the working directory:

..  code-block:: shell

    mkdir istsos3-plugin-name
    cd istsos3-plugin-name
    mkdir lib
    touch .babelrc .eslintrc .gitignore .npmignore README.md
    touch lib/index.js
    touch lib/config.js

Than initialize the npm package

..  code-block:: shell

    npm init

If you have an npm organization scope:

..  code-block:: bash

    npm init --scope=YOUR-ORG-NAME

Add all the required dependencies for the development.

..  code-block:: bash

    yarn add --dev \
        babel-cli \
        babel-core \
        babel-eslint \
        babel-preset-env \
        babel-preset-react \
        eslint eslint-plugin-import \
        eslint-plugin-jsx-a11y \
        eslint-plugin-react \
        eslint-watch \
        babel-plugin-transform-object-rest-spread \
        react \
        react-dom \

Add istsos3 dependencies:

 - istsos3-core contains fetching capabilities to execute istSOS3 actions.
 - istsos3-ui contains some reusable istSOS3 web widgets

..  code-block:: bash

    yarn add \
        @istsos/istsos3-core \
        @istsos/istsos3-ui

To develop using the Semantic UI framework

..  code-block:: bash

    yarn add --dev \
        semantic-ui-react \
        semantic-ui-css

Fill the babel presets file .babelrc with this configuration

..  code-block:: json

    {
        "presets": ["env", "react"],
        "plugins": [
            "transform-object-rest-spread"
        ]
    }

Modify the package.json file scripts like this

..  code-block:: json

    {
        "scripts": {
            "build": "babel lib -d build",
            "build:watch": "babel lib -w -d build",
            "lint": "eslint lib/**; exit 0",
            "lint:watch": "esw -w lib/**",
            "prepublish": "npm run build"
        }
    }

Creates a symbolic link from a global folder

..  code-block:: bash

    npm link

If working with source code of istsos3-core and istsos3-ui, link them globally
as in the previews command then link them to you plugin

..  code-block:: bash

    npm link @istsos/istsos3-core
    npm link @istsos/istsos3-ui

Go in the istsos3-admin folder and link your plugin

..  code-block:: bash

    npm link YOUR_PLUGIN_NAME

To start the development, cd to your plugin folder

..  code-block:: bash

    npm run build:watch

Then also start the istsos3-admin module. cd to its folder and

..  code-block:: bash

    npm start

To Build the component

..  code-block:: bash

    yarn build
