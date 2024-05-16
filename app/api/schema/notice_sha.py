def notice_args_valid(parser):
    parser.add_argument('title', type=str)
    parser.add_argument('content', type=str)