def user_collect_args_valid(parser):
    parser.add_argument('collection_id', type=int, location='collection_id')
    parser.add_argument('user_id', type=int, location='json')
    parser.add_argument('book_id', type=int, location='json')
