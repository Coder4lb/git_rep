import recommendations , json

count = 10
with open("rateset.txt" , 'r' ) as data:
	critics = json.loads(data.read())

rs = recommendations.getRecommendations(critics , 'user2')[:count]

with open("id_title_set.txt" , 'r' , encoding='utf-8') as data:
	it = eval(data.read())

for item in rs:
	id = int(item[1])
	print(item[0],item[1],it[id])