
from twisted.protocols.basic import Int32StringReceiver
from planes.python.xml.tags import Tag

class Channel(Int32StringReceiver):
    def stringReceived(self, string):
        self.tagsReceived(Tag.parseString(string))
    def sendTags(self, document):
        self.sendString(document.xml)

class Factory(ServerFactory):
    protocol = Channel

Tags = Channel
TagsChannel = Channel
TagsFactory = Factory

