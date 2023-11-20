# -*- coding: utf-8 -*-

import easytrader
import yaml

trades = {
    'balance': lambda user: print(user.balance),
    'position': lambda user: print(user.position),
    'today_trades': lambda user: print(user.today_trades),
    'refresh': lambda user: user.refresh(),
    'auto_ipo': lambda user: print(user.auto_ipo()),
    'cancel_entrust': lambda user: user.cancel_entrust('123456'),
    'cancel_all_entrusts': lambda user: user.cancel_all_entrusts(),
    'today_entrusts': lambda user: print(user.today_entrusts),
    'buy': lambda user: user.buy(),
    'sell': lambda user: user.sell(),
    'all_cond_trades': lambda user: print(user.all_cond_trades),
    'repo': lambda user: user.repo(),
    'reverse_repo': lambda user: user.reverse_repo(),
    'cond_trades': lambda user: print(user.cond_trades),
    'conf_buy': lambda user: user.conf_buy('123456'),
    'conf_sell': lambda user: user.conf_sell('123456'),
    'cancel_conf_trade': lambda user: user.cancel_conf_trade('123456'),
    'cancel_conf_trades': lambda user: user.cancel_conf_trades('123456'),
    'unlock': lambda user: user.unlock,
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
        user = easytrader.use(account["name"], debug=True)

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



def test_yh_client(file_path):
    print('start to connect yh client...')
    user = easytrader.use('yh_client')
    user.prepare(file_path)

    print(f'balance: {user.balance}')

    print(f'today_entrusts: {user.today_entrusts}')
    print(f'today_trades: {user.today_trades}')
    print(f'cancel_entrusts: {user.cancel_entrusts}')

    result = user.cancel_entrust("123456789")
    print(f'cancel_invalid_entrusts: {result}')

    try:
        result = user.buy("511990", 1, 1e10)
        print(f'invalid_buy: {result}')
    except Exception as e:
        print(e)

    try:
        result = user.sell("162411", 200, 1e10)
        print(f'invalid_sell: {result}')
    except Exception as e:
        print(e)

    try:
        result = user.auto_ipo()
        print(f'invalid_sell: {result}')
    except Exception as e:
        print(e)

def main():
    try:
        accounts = load_accounts()
        for account in accounts['accounts']:
            exec_account(account)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
    # test_yh_client('./yh_client.json')