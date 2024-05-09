def email_verify_args_valid(parser):
    parser.add_argument('email', type=str, location='json')
    parser.add_argument('mode', type=int, location='json')
    parser.add_argument('captcha', type=str, location='json')