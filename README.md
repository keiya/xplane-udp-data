# xplane-udp-data

X-Plane 10のネットワーク経由data inputを解析します。

## X-Planeが送信するUDPの構造
バイトオーダーはLittle-endian(Pythonのsocketが変換しているのかも？)
```
char[] 'DATA@' // 固定, 5bytes

// このstructのalignmentは4bytes
// X-Planeで複数のdataを出力するとこれが連なる
struct[] {
    int // 4bytes, dataのid(X-planeのチェックボックスに対応)
    float // 4bytes, 実際のデータ
}
```
現在のところ、structの大きさはint[4bytes]+(float[4bytes]+align[4bytes])\*4にて36bytes。
複数のdataを送るようにすると、このあとに4bytesのalignが入る。
```
'DATA@' + struct + (align) + struct + (align) + struct + (align) + ....
```
