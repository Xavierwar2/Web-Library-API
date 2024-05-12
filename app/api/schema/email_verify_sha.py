def email_verify_args_valid(parser):
    parser.add_argument('email', type=str)
    parser.add_argument('mode', type=int)
    parser.add_argument('captcha', type=str)
