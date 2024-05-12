def reg_args_valid(parser):
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('status', type=int)
    parser.add_argument('captcha', type=str)
