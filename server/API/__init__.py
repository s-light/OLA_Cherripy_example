# -*- coding: utf-8 -*-

"""
Cherrypy API package.

(for cherrypy server)


Operations:
    (http://www.ibm.com/developerworks/library/ws-restful/index.html#N10066)
    - To create a resource on the server, use POST.
    - To retrieve a resource, use GET.
    - To change the state of a resource or to update it, use PUT.
    - To remove or delete a resource, use DELETE.
"""

import cherrypy

##########################################


class Channel(object):

    """
    API for channel settings.

        GET = receive channel value(s)
        PUT = set channel value
    """

    exposed = True

    def __init__(self):
        """define sub mapping for targettimes and tags."""
        self.channel_names = {
            'channel_request': 'ola-channel-request',
            'channel_response': 'ola-channel-response',
            'channel_set': 'ola-channel-set',
        }

    # @cherrypy.expose
    # @cherrypy.tools.json_in()
    # @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self, channel_id=None):
        """
        Return channel information.

            if channel_id=None returns list of channel values.
            if channel_id is digit returns single channel value
        """
        # print("Channel GET:")
        # print("  channel_id:{}".format(channel_id))
        # print("  args:{}".format(args))
        result = {}
        temp = cherrypy.engine.publish(
            self.channel_names['channel_request'],
            channel_id=channel_id
        )
        # print("temp: {}".format(temp))
        # result = temp
        if channel_id:
            result = temp
        elif channel_id is None:
            # print("channel list")
            # result = temp.tolist()
            result = temp[0].tolist()
        # elif cherrypy.response.status != 404:
        #     print("list users")
        #     raw_result = self.db.query(DBModel.User).all()
        #     result = []
        #     # print(raw_result)
        #     for u in raw_result:
        #         result.append(u.tojson())
        else:
            result = "ERROR ?!"
        # print("\nresult: {}\n".format(result))
        # cherrypy.response.headers['Content-Transfer-Encoding'] = 'utf-8'
        # print(cherrypy.response.headers)
        return result

    @cherrypy.tools.json_out()
    def PUT(self, channel_id=None, channel_value=None):
        """set channel information."""
        print("Channel PUT:")
        print("  channel_id:{}".format(channel_id))
        print("  channel_value:{}".format(channel_value))
        result = {}
        temp = cherrypy.engine.publish(
            self.channel_names['channel_set'],
            channel_id=channel_id,
            channel_value=channel_value
        )
        # print("temp: {}".format(temp))
        # result = temp
        if temp:
            result = temp
        else:
            result = "ERROR ?!"
        return result

    @cherrypy.tools.json_out()
    def POST(self, channel_id=None, channel_value=None):
        """set channel information."""
        print("Channel POST:")
        print("  channel_id:{}".format(channel_id))
        print("  channel_value:{}".format(channel_value))
        result = {}
        temp = cherrypy.engine.publish(
            self.channel_names['channel_set'],
            channel_id=channel_id,
            channel_value=channel_value
        )
        # print("temp: {}".format(temp))
        # result = temp
        if temp:
            result = temp
        else:
            result = "ERROR ?!"
        return result


class APIHandler(object):

    """API Handler - delegate sub calls to there API parts."""

    exposed = True

    def __init__(self):
        """define routs."""
        self.channel = Channel()

    # @cherrypy.expose
    # def index(self):
    #     pass

    # @cherrypy.expose
    def GET(self):
        """return some API example calls/information."""
        info = """Welcome to the API :-) <br>
        try one of the following:
        <ul>
            <li><a href="channel/">channel/</a></li>
            <li><a href="channel/1/">channel/1/</a></li>
            <li><a href="channel/5/">channel/5/</a></li>
            <li><a href="channel/512/">channel/512/</a></li>
        </ul>
        <form action="/api/channel/" method="post">
            <label>
                channel_id
                <input
                    type="number"
                    id="channel_id"
                    name="channel_id"
                    maxlength="5"
                    value="3"
                >
            </label>
            <label>
                channel_value
                <input
                    type="number"
                    id="channel_value"
                    name="channel_value"
                    maxlength="5"
                    value="111"
                >
            </label>
            <button type="submit">send</button>
        </form>
        """
        return info


if __name__ == '__main__':
    print("""demo for this tool""")
    configAPI = {
        '/': {
            'tools.sessions.on': True
        },
        '/api': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        }
    }
    APIHandlerInstance = APIHandler()
    cherrypy.tree.mount(APIHandlerInstance, '/api', configAPI)
