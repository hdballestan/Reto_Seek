from decouple import config, Csv
HOST_ = config('HOST', default='localhost')
PORT_ = int(config('PORT'))
USERNAME_ = config('USERNAME', default='')
DBPASS_ = config('DBPASS', default='')
SOURCE_ = config('SOURCE', default='')
CLIENT_ = config('CLIENT', default='')

