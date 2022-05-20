from redis import StrictRedis
import os
import time
import json
import pcg_processing as pcg
import config


class HeartWorker():
    def __init__(self) -> None:
        redis_url = f'redis://{config.redis_host}:{config.redis_port}/{config.redis_db}'
        self.redis = StrictRedis.from_url(url=redis_url)
        self.key = f'{config.redis_app}:task'
        self.pcg = pcg.PcgProc()

    def work(self):
        """ Обработка файлов """
        while True:
            task = self.redis.lpop(self.key)
            if not task:
                time.sleep(1)
                continue

            task = json.loads(task)

            if task['id'] == 'pcg':
                if task['type'] == 'file':
                    reports = self.pcg.processing(task['value'], self.redis)
                    user_id = task['user_id']
                    for r in reports:                        
                        cmd = {'user_id': user_id,
                               'type': r['t'], 
                               'value': r['v']}
                        self.redis.rpush(
                            f'{config.app_name}:cmd', json.dumps(cmd))
                    # TODO сделать управление удалением файлов
                    # os.remove(task['value'])


if __name__ == '__main__':
    hw = HeartWorker()
    hw.work()
