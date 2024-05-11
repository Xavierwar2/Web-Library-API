def admin_args_valid(parser):
    parser.add_argument('username', type=str, location='json')
    parser.add_argument('password', type=str, location='json')
    parser.add_argument('is_super_admin', type=int, location='json')
