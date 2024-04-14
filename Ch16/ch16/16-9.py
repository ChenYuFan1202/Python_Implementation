import face_module as m   # 匯入自訂模組

base = 'https://japanwest.api.cognitive.microsoft.com/face/v1.0'     # api
key = '您的金鑰'                                                      # 你的金鑰
gid = 'gp01'                                                         # 群組 Id
pid = '8d649904-55b4-4dce-a834-b4dfcdb0b667'                         # 成員 Id

m.face_init(base, key)  # 初始化端點和金鋪
m.face_use(gid, pid)    # 指定要操作的 gid 和 pid
m.face_shot('add')      # 不斷進行拍照並上傳到Azuse新增成員人臉影像
