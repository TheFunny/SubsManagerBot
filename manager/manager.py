import hashlib
import json
import os

from text import PROFILE_TEMPLATE


class Data:
    def __init__(self, filename):
        self.path = f'data/{filename}.json'
        self.data = self.load_data(self.path)

    @staticmethod
    def load_data(path):
        path_dir = os.path.split(path)[0]
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

            return {}
        with open(path, 'r+', encoding='utf-8') as f:
            data = f.read()
            if data == '':
                return {}
            return json.loads(data)

    @staticmethod
    def save_data(path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def save_file(path, data):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)

    def save(self):
        self.save_data(self.path, self.data)


class Manager(Data):
    def __init__(self, filename):
        super().__init__(filename)
        self.server: dict = self.load_server()
        self.server_seq: dict = self.load_server_seq()
        self.user: dict = self.load_user()
        self.url: str = self.load_url()
        self.pw: str = self.load_pw()

    def load_server(self) -> dict:
        if 'server' not in self.data:
            return {}
        return self.data['server']

    def load_server_seq(self) -> dict:
        if 'server_seq' not in self.data:
            return {}
        return self.data['server_seq']

    def load_user(self) -> dict:
        if 'user' not in self.data:
            return {}
        return self.data['user']

    def load_url(self) -> str:
        if 'url' not in self.data:
            return ''
        return self.data['url']

    def load_pw(self) -> str:
        if 'pw' not in self.data:
            return ''
        return self.data['pw']

    def save(self):
        self.data['server'] = self.server
        self.data['server_seq'] = self.server_seq
        self.data['user'] = self.user
        self.data['url'] = self.url
        self.data['pw'] = self.pw
        super().save()

    def set_url(self, url: str) -> bool:
        self.url = url.strip('/')
        self.save()
        return True

    def set_pw(self, pw: str) -> bool:
        self.pw = pw
        self.save()
        return True

    def get_url_pw(self) -> tuple[str, str]:
        return self.url, self.pw

    def server_id_max(self) -> int:
        return int(max(self.server.keys())) if self.server != {} else 0

    def server_seq_init(self) -> None:
        if self.server_seq != {}:
            if len(self.server_seq) != len(self.server):
                for server_id in filter(lambda x: x not in self.server_seq, self.server):
                    self.server_seq[server_id] = len(self.server_seq)
                self.save()
            return
        for server_seq, server_id in enumerate(self.server):
            self.server_seq[server_id] = server_seq
        self.save()

    def change_server_seq(self, server_id: str, target_pos: str) -> bool:
        self.server_seq_init()
        target_pos = int(target_pos)
        original_pos: int = self.server_seq[server_id]
        if server_id not in self.server:
            return False
        if target_pos not in self.server_seq.values():
            return False
        if original_pos == target_pos:
            return True
        server_seq_sorted = filter(
            lambda x: min(original_pos, target_pos) <= x[1] <= max(original_pos, target_pos),
            sorted(self.server_seq.items(), key=lambda x: x[1])
        )
        for server_id, pos in server_seq_sorted:
            if pos == original_pos:
                self.server_seq[server_id] = target_pos
            else:
                self.server_seq[server_id] += 1 if original_pos > target_pos else -1
        self.save()
        return True

    def add_server(self, name: str) -> bool:
        if name in self.server.values():
            return False
        self.server[str(self.server_id_max() + 1)] = name
        self.save()
        return True

    def remove_server(self, server_id: str) -> bool:
        if server_id not in self.server:
            return False
        del self.server[server_id]
        del self.server_seq[server_id]
        for user in self.user.values():
            if server_id in user['server']:
                del user['server'][server_id]
            if user['server'] == {}:
                user['server'] = None
        self.save()
        return True

    def rename_server(self, server_id: str, new_name: str) -> bool:
        if server_id not in self.server:
            return False
        if new_name in self.server.values():
            return False
        self.server[server_id] = new_name
        self.save()
        return True

    def get_server_name(self, server_id: str) -> str:
        return self.server[server_id]

    def get_server_enum(self) -> list:
        self.server_seq_init()
        return sorted(self.server.items(), key=lambda x: self.server_seq[x[0]])

    @staticmethod
    def gen_md5(name: str) -> str:
        return hashlib.md5(name.encode('utf-8')).hexdigest()[8:-8]

    def add_user(self, name: str) -> bool:
        if name in self.user.values():
            return False
        self.user[name] = {"link": self.gen_md5(name), "server": None, 'target': 'mixed'}
        self.save()
        return True

    def remove_user(self, name: str) -> bool:
        if name not in self.user:
            return False
        del self.user[name]
        self.save()
        return True

    def rename_user(self, old_name: str, new_name: str) -> bool:
        if old_name == new_name:
            return False
        if old_name not in self.user:
            return False
        self.user[new_name] = self.user[old_name]
        del self.user[old_name]
        self.save()
        return True

    def set_user_target(self, user_name: str, target: str) -> bool:
        if user_name not in self.user:
            return False
        self.user[user_name]['target'] = target
        self.save()
        return True

    def get_user_target(self, user_name: str) -> str:
        return self.user[user_name].get('target', 'unset')

    def get_user_list(self) -> list:
        return list(self.user.keys())

    def add_sub(self, name: str, server_id: str, link: str) -> bool:
        if name not in self.user:
            return False
        if server_id not in self.server:
            return False
        sub = self.user[name]['server']
        if sub is None:
            self.user[name]['server'] = {server_id: link}
        else:
            sub[server_id] = link
        self.save()
        return True

    def remove_sub(self, name: str, server_id: str) -> bool:
        if name not in self.user:
            return False
        if server_id not in self.user[name]['server']:
            return False
        del self.user[name]['server'][server_id]
        if self.user[name]['server'] == {}:
            self.user[name]['server'] = None
        self.save()
        return True

    def get_sub_user(self, server_id: str) -> list:
        return [name for name in self.user if
                self.user[name]['server'] is not None and server_id in self.user[name]['server']]

    def get_user_sub(self, name: str) -> list:
        if name not in self.user:
            return []
        return [link for link in self.user[name]['server'].values()] if self.user[name]['server'] is not None else []

    def get_link(self, user: str) -> str:
        return self.user[user]['link']

    def get_link_enum(self) -> list:
        return [(name, self.get_link(name)) for name in self.user]

    def export_user_sub(self) -> list[(str, str)]:
        subs = []
        for user_name in self.get_user_list():
            sub = self.get_user_sub(user_name)
            sub = "|".join(sub) if sub != [] else ""
            target = self.get_user_target(user_name)
            target = target if target != 'unset' else 'mixed'
            subs.append((self.get_link(user_name), PROFILE_TEMPLATE.format(sub=sub, target=target)))
        return subs

    def save_sub(self, subs=None) -> bool:
        if subs is None:
            subs = self.export_user_sub()
        if not os.path.exists('sub'):
            os.makedirs('sub')
        for filename in os.listdir('sub'):
            try:
                os.remove(f'sub/{filename}')
            except Exception as e:
                print(e)
                return False
        for filename, sub in subs:
            if sub == "":
                continue
            self.save_file(f'sub/{filename}.ini', sub)
        return True
