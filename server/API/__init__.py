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

##########################################
# Helper tools
# http://docs.cherrypy.org/en/latest/extend.html#request-parameters-manipulation


class ChannelTool(cherrypy.Tool):

    """
    convert request channel parameters.

    cherrypy tool to automatically convert
    requests with json channel information to request parameters.
    """

    def __init__(self):
        """setup cherrypy tool."""
        cherrypy.Tool.__init__(self, 'before_handler', self.load, priority=90)

    # def load(self, debug=False):
    def load(self):
        """converte request channel info to request parameters."""
        req = cherrypy.request
        # if debug:
        # #     print(42*"§")
        # print(" ")
        # print(42*"§")
        # print("params:")
        # for key, value in req.params.items():
        #     print(" {}:{}".format(key, value))
        # print(42*"§")
        # print(" ")

        result_channel_id = None
        result_channel_value = None
        try:
            req_json = req.json
        except AttributeError:
            # no json
            # print("no json part found.")
            pass
        else:
            # print("  req_json:{}".format(req_json))
            # print("try to extract channel_id and channel_value:")
            # result_channel_id = getattr(req_json, 'channel_id', None)
            # result_channel_value = getattr(req_json, 'channel_value', None)
            try:
                result_channel_id = req_json['channel_id']
            except AttributeError:
                result_channel_id = None
            try:
                result_channel_value = req_json['channel_value']
            except AttributeError:
                result_channel_value = None
            # print("  result_channel_id:{}".format(result_channel_id))
            # print("  result_channel_value:{}".format(result_channel_value))

        req.params['channel_id'] = result_channel_id
        req.params['channel_value'] = result_channel_value

cherrypy.tools.ola_channels = ChannelTool()


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
    # @cherrypy.tools.ola_channels()
    @cherrypy.popargs('channel_id')
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
        if channel_id is not None:
            result = temp
        else:
            # elif channel_id is None:
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
        # else:
        #     result = "ERROR ?!"
        # print("\nresult: {}\n".format(result))
        # cherrypy.response.headers['Content-Transfer-Encoding'] = 'utf-8'
        # print(cherrypy.response.headers)
        return result

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.ola_channels()
    @cherrypy.popargs('channel_id')
    @cherrypy.popargs('channel_value')
    def PUT(self, channel_id=None, channel_value=None):
        """set channel information."""
        print("Channel PUT:")
        print('params: {}'.format(cherrypy.request.params))
        jsondata = cherrypy.request.json
        print('request.json: {}'.format(jsondata))
        print("  channel_id:{}".format(channel_id))
        print("  channel_value:{}".format(channel_value))
        result = {}
        temp = cherrypy.engine.publish(
            self.channel_names['channel_set'],
            channel_id=channel_id,
            channel_value=channel_value
        )[0]
        # print("temp: {}".format(temp))
        # result = temp
        if temp:
            result = {
                'channel_id': channel_id,
                'channel_value': temp,
            }
        else:
            result = "ERROR ?!"
        return result

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.ola_channels()
    def POST(self, channel_id=None, channel_value=None):
        """set channel information."""
        # print("Channel POST:")
        # print("  channel_id:{}".format(channel_id))
        # print("  channel_value:{}".format(channel_value))
        result = {}
        temp = cherrypy.engine.publish(
            self.channel_names['channel_set'],
            channel_id=channel_id,
            channel_value=channel_value
        )[0]
        # print("temp: {}".format(temp))
        # result = temp
        if temp:
            result = {
                'channel_id': channel_id,
                'channel_value': temp,
            }
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
