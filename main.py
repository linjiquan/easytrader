# -*- coding: utf-8 -*-

import easytrader
import yaml

trades = {
    'balance': lambda user: print(user.balance),
    'position': lambda user: print(user.position),
    'today_trades': lambda user: print(user.today_trades),
    'buy': lambda user: print('action skipped'),
    'sell': lambda user: print('action skipped'),
}


def load_accounts(filepath='./accounts.yml'):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def exec_account_actions(user, account):
    actions = account['actions'] if 'actions' in account.keys() else []

    for action in actions:
        print(f'exec action {action}...')
        trades[action](user)


def exec_account(account):
    name = account['name'] if 'name' in account.keys() else None
    status = account['status'] if 'status' in account.keys() else 1
    exe_path = account['exe_path'] if 'exe_path' in account.keys() else None
    username = account['user'] if 'user' in account.keys() else None
    comm_password = account['comm_password'] if 'comm_password' in account.keys() else None
    password = account['password'] if 'password' in account.keys() else None
    cookies = account['cookies'] if 'cookies' in account.keys() else None
    portfolio_code = account['portfolio_code'] if 'portfolio_code' in account.keys() else None

    print(f'\nexec account {name} with name {username}...')

    if name is None:
        print('Invalid account as its name is empty')
        return

    if status == 0:
        print(f'skipped account {name} as it is disabled')
        return

    try:
        user = easytrader.use(account["name"])

        print('preparing account...')
        # user.prepare('./yh_client.json')
        user.prepare(exe_path=exe_path, user=username,
                     password=password, comm_password=comm_password,
                     cookies=cookies, portfolio_code=portfolio_code)

        exec_account_actions(user, account)

    except Exception as e:
        print(f'exec account failed, error: {e}')

    finally:
        user.exit()


def main():
    try:
        accounts = load_accounts()
        for account in accounts['accounts']:
            exec_account(account)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
