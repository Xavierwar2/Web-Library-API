def comment_args_valid(parser):
    parser.add_argument('content', type=str, location='json')
    parser.add_argument('user_id', type=int, location='json')
    parser.add_argument('book_id', type=int, location='json')
    parser.add_argument('delete_list', type=list, location='json')
