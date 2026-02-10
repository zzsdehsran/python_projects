import requests

def download_and_save_ips(url, filepath):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate, br, zstd',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'path':'/china-operator-ip/chinanet.txt',
    }
    try:
        # 尝试连接
        print(f"正在连接{url}...")
        response = requests.get(url, headers=headers,timeout=10)

        # 检查http状态码
        response.raise_for_status()
        
        #指定编码类型去解码
        response.encoding = 'utf-8'
        # response.encoding = response.apparent_encoding
        

        # 处理数据
        data = response.text.strip()
        print(data)
        count = len(data.split())
        print(f"获取成功，共{count}条数据。")

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(data)
        print(f"文件已保存至：{filepath}")

    except Exception as e:
        print(f"错位原因：{e}")

if __name__ == '__main__':
    target  = 'https://gaoyifan.github.io/china-operator-ip/chinanet.txt'
    file = 'chinanet_safe.txt'

    download_and_save_ips(target, file)