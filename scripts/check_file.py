with open('ic_card_app/pages/index/index.vue', 'rb') as f:
    content = f.read()
    lines = content.split(b'\n')
    for i, line in enumerate(lines[7:9], start=8):
        print(f'Line {i}: {line}')
        print(f'Line {i} decoded: {line.decode("utf-8")}')
        print()
