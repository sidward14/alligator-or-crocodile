import asyncio
loop = asyncio.get_event_loop()
from io import BytesIO

import responder
import aiohttp
from fastai import *
from fastai.vision import *

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

api = responder.API( cors = True )

path = Path(__file__).parent

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# First download the pickled model from url and then unpickle it:

export_file_url = 'https://www.dropbox.com/s/cot6bbu4w4dteei/trained_learner_allicroc.pkl?raw=1'
export_file_name = 'trained_learner_allicroc.pkl'

async def download_file( url, dest ):
  if dest.exists(): return
  async with aiohttp.ClientSession() as sess:
    async with sess.get( url ) as resp:
      data = await resp.read()
      with open( dest, 'wb' ) as f: f.write( data )

async def setup_learner():
  await download_file( url = export_file_url, dest = path/'models'/export_file_name )
  try:
    learn = load_learner( path = path/'models', fname = export_file_name )
    return learn
  except RuntimeError as e:
    if len( e.args ) > 0 and 'CPU-only machine' in e.args[0]:
      print( e )
      message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
      raise RuntimeError(message)
    else:
      raise

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# Set up routing for the web service:

@api.route( '/' )
def index( req, resp ):
  html = path/'index.html'
  resp.html = html.open().read()

@api.route( '/classify' )
async def classify( req, resp ):
  data = await req._starlette.form()
  img_bytes = await ( data[ 'file' ].read() )
  img = open_image( fn = BytesIO( img_bytes ) )
  prediction = learn.predict( img )[ 0 ]
  resp.media = { 'result': str( prediction ) }

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

if __name__ == '__main__':

  tasks = [ asyncio.ensure_future( setup_learner() ) ]
  learn = loop.run_until_complete( asyncio.gather( *tasks ) )[0]
  loop.close()

  if 'serve' in sys.argv: api.run()
