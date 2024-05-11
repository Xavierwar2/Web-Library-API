def user_args_valid(parser):
    parser.add_argument('user_id', type=int, location='user_id')
    parser.add_argument('username', type=str, location='username')
    parser.add_argument('email', type=str, location='email')
    parser.add_argument('sex', type=int, location='sex')
    parser.add_argument('age', type=int, location='age')
    parser.add_argument('status', type=int, location='status')
    parser.add_argument('image_url', type=str, location='image_url')
