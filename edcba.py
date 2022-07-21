import sys
import discid
import musicbrainzngs
import subprocess
import shlex

from pprint import pprint


disc = discid.read()  # use default device
pprint("id: %s" % disc.id) # Python 3
#pprint( vars(disc)['_handle'] )


musicbrainzngs.set_useragent("edcba cd ripper", "0.1", "")

try:
    #result = musicbrainzngs.get_releases_by_discid(disc.id,includes=["artists"])
    result = musicbrainzngs.get_releases_by_discid(disc.id,includes=["artists", "recordings"])
    #pprint( result )
    #pprint( result["disc"]["release-list"][0] )
    #pprint( result["disc"]["release-list"][0]['id'] )
except musicbrainzngs.ResponseError:
    print("disc not found or bad response")
    raise Exception

if result.get("disc"):
    #print("artist:\t%s" % result["disc"]["release-list"][0]["artist-credit-phrase"])
    #print("title:\t%s" % result["disc"]["release-list"][0]["title"])
    r_index='disc'
elif result.get("cdstub"):
    r_index='cdstub'
    #print("artist:\t" % result["cdstub"]["artist"])
    #print("title:\t" % result["cdstub"]["title"])
else:
    raise Exception

#FIXME: Hardcoded to the first entry only for the disc_id
try:
    release_id = result[r_index]["release-list"][0]['id']
    release_artist = result[r_index]["release-list"][0]['artist-credit-phrase']
    release_title = result[r_index]["release-list"][0]['title']
    release_track_list = result[r_index]["release-list"][0]['medium-list'][0]['track-list']
except KeyError:
    pprint( "Couldnt find values" )
    raise Exception

#pprint( "Release id: %s" %( release_id ) )
#pprint( "Release artist: %s" %( release_artist ) )
#pprint( "Release title: %s" %( release_title ) )
pprint( "Release release_track_list: %s" %( release_track_list[0]  ) )

try:
    cover_art_list = musicbrainzngs.get_image_list( release_id )
    #pprint( cover_art_list )
    #pprint( cover_art_list['images'][0]['image'] )
except Exception:
    pprint( "Couldnt find values" )
    raise Exception

wav_file = "abcde.820a8a0b/track01-moo.wav"
enc_file = "abcde.820a8a0b/track01-moo.ogg"
rip_command = shlex.split( "%s -d %s %s %s"%("cdparanoia", "/dev/sr0", "01", "abcde.820a8a0b/track01-moo.wav") )
try:
    p1 = subprocess.check_call(rip_command, stdout=subprocess.PIPE)
except subprocess.CalledProcessError:
    pprint( "cdparadnoia failed" )
    raise Exception

encoder='oggenc'
encode_command=shlex.split( "%s %s --output %s"%(encoder, wav_file, enc_file) )
try:
    p1 = subprocess.check_call( encode_command, stdout=subprocess.PIPE)
except subprocess.CalledProcessError:
    pprint( "encoder failed" )
    raise Exception

