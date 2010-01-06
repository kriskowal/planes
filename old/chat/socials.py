#!/usr/bin/env python

from cixar.ish.sh.inoculate import inoculate

emote_url = '.chat/art/tango'

def social(template, verb, verbs, implicit_modifier = None):

    @command()
    def social(self, object = None, modifier = None):

        subject = inoculate(self.name)

        # if the user specified a modifier, it's going to be
        #  the second argument instead of the last, so switch
        #  the variables around (this makes it possible to use
        #  the default argument for the explicit modifier case).
        if modifier is not None:
            object, modifier = modifier, object
        # otherwise, use the implicit modifier
        else:
            modifier = implicit_modifier

        # conjugate the predicate
        if object is None:
            predicate = verb
            predicates = verbs
        else:   
            object = inoculate(object)
            if modifier is None:
                predicate = '%s %s' % (verb, object)
                predicates = '%s %s' % (verbs, object)
            else:
                modifier = inoculate(modifier)
                predicate = '%s %s %s' % (verb, modifier, object)
                predicates = '%s %s %s' % (verbs, modifier, object)

        self.message(template % ('You', predicate))
        self.broadcast(template % (subject, predicates))

    return social

smile = social(
   '''%%s %%s. <img src="%s/face-smile.png" alt=":-)"/>''' % emote_url,
   'smile', 'smiles', 'at'
)
gawk = social(
   '''%%s %%s. <img src="%s/face-smile-big.png" alt=":-D"/>''' % emote_url,
   'gawk', 'gawks', 'at'
)
grin = social(
   '''%%s %%s. <img src="%s/face-devil-grin.png" alt=">:-)"/>''' % emote_url,
   'grin evily', 'grins evily', 'at'
)
cry = social(
   '''%%s %%s. <img src="%s/face-crying.png" alt=":'("/>''' % emote_url,
   'cry', 'cries'
)
kiss = social(
   '''%%s %%s. <img src="%s/face-kiss.png" alt=":-*"/>''' % emote_url,
   'kiss', 'kisses',
)
wink = social(
   '''%%s %%s. <img src="%s/face-wink.png" alt=";-)"/>''' % emote_url,
   'wink', 'winks', 'at'
)
pout = social(
   '''%%s %%s. <img src="%s/face-sad.png" alt=":-("/>''' % emote_url,
   'pout', 'pouts'
)
shrug = social(
   '''%%s %%s. <img src="%s/face-plain.png" alt=":-|"/>''' % emote_url,
   'shrug', 'shrugs'
)
dance = social(
    '%s %s.',
    'dance', 'dances', 'with'
)

