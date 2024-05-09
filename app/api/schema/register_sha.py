def reg_args_valid(parser):
    parser.add_argument('username', type=str, location='json')
    parser.add_argument('password', type=str, location='json')
    parser.add_argument('email', type=str, location='json')
    parser.add_argument('status', type=int, location='json')
    parser.add_argument('captcha', type=str, location='json')
