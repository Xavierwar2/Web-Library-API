def user_args_valid(parser):
    parser.add_argument('user_id', type=int, help='user_id')
    parser.add_argument('username', type=str, help='username')
    parser.add_argument('email', type=str, help='email')
    parser.add_argument('sex', type=int, help='sex')
    parser.add_argument('age', type=int, help='age')
    parser.add_argument('status', type=int, help='status')
    parser.add_argument('image_url', type=str, help='image_url')
