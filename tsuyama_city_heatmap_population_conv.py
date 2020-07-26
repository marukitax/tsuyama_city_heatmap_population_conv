#
# 津山市オープンデータ（施設情報変換）
#
import sys
import argparse
import csv
import codecs

print ('＊津山市オープンデータ変換：当月分人口集計（ヒートマップ）')

def get_args():

	parser = argparse.ArgumentParser()

	parser.add_argument("inputCSV",  help="入力ＣＳＶ（オープンデータＣＳＶ）", type=str)
	parser.add_argument("chikuCSV",  help="地区ＣＳＶ（地区CD緯度経度ＣＳＶ）", type=str)
	parser.add_argument("outputCSV", help="出力ＣＳＶ（アップロード用ＣＳＶ）", type=str)

	args = parser.parse_args()

	return(args)

def main():
	args = get_args()

	print ("入力ＣＳＶ："+args.inputCSV)
	print ("地区ＣＳＶ："+args.chikuCSV)
	print ("出力ＣＳＶ："+args.outputCSV)

	# 地区コード位置情報テーブル作成
	chiku_data_i = []
	chiku_data   = []
	with open(args.chikuCSV, 'r') as f_in2:
			reader = csv.reader(f_in2)
			header = next(reader)	# ヘッダー読み飛ばし
			for row in reader:
				chiku_data_i.append(row[0])					# 地区コード
				chiku_data.append([row[1],row[2],row[3]])	# 地区名、緯度、経度

	# オープンデータＣＳＶ⇒アップロード用ＣＳＶ作成
	with codecs.open(args.inputCSV, 'r', 'utf_16') as f_in1:
		with open(args.outputCSV, 'w', encoding="utf_8_sig") as f_ot1:
			reader = csv.reader(f_in1)
			writer = csv.writer(f_ot1,lineterminator='\n')
			writer.writerow(['地区ＣＤ','集計年月','緯度','経度','地区名','日本人男','日本人女','外国人男','外国人女'])
			header = next(reader)	# ヘッダー読み飛ばし
			for row in reader:
				chikucd = row[0][0:6]
				if chikucd != '999999':		# 合計行読み飛ばし
					data = [chikucd,row[1]]														# 地区ＣＤ、集計年月
					if chikucd in chiku_data_i:		# 地区コードから地区情報設定
						idx = chiku_data_i.index(chikucd)
						data.extend([chiku_data[idx][1],chiku_data[idx][2],chiku_data[idx][0]])	# 緯度、経度、地区名
					else:
						data.extend(['0.0','0.0','地区ＣＤエラー'])								# 緯度、経度、地区名（地区エラー）
					data.extend([row[2],row[3],row[5],row[6]])									# 日本人男、日本人女、外国人男、外国人女
					writer.writerow(data)

if __name__ == '__main__':
	main()

