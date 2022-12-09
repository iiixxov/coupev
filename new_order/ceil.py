class Ceil:
    @staticmethod
    def get_doors_sizes(L, n, sizes, perehselt, gorizont):
        count = 0
        L += perehselt
        for i in range(n):
            if sizes[i] != 0:
                L -= sizes[i]
            else:
                count += 1
        for i in range(n):
            if sizes[i] == 0:
                sizes[i] = L / count
        return sizes

    @staticmethod
    def get_sizes(H, L, n, div, d_sizes):
        """
        :param H: высота проема
        :param L: длинна проема
        :param n: количество дверей
        :param div: разделить двери на части
        """
        sizes = list()
        for i in range(n):
            h_div, l_div = div[i]
            # doors
            sizes.append([])
            y, y1 = 0, 0
            for j in range(h_div):
                # cols
                sizes[i].append([])
                y = y1
                y1 += H / h_div
                if i == 0:
                    x, x1 = 0, 0
                else:
                    x, x1 = x1 + 50, x1 + 50
                for _ in range(l_div):
                    x1 += d_sizes[i] / l_div
                    g = list(map(lambda size: round(size), (x, y, x1, y1)))
                    # elem
                    sizes[i][j].append(g)
                    x = x1
        print(sizes)
        return sizes

    @staticmethod
    def change_sizes(door_sizes, div, changes, height, long):
        """
        :param door_sizes: размер из get_sizes()
        :param div: разделить двери на части
        :param changes: изменить размеры на
        :param height: высота двери
        :param long: длинна двери
        """
        height_div, long_div = div
        height_sizes, long_sizes = changes
        zero_x = len(tuple(filter(lambda a: a == 0, long_sizes)))
        zero_y = len(tuple(filter(lambda a: a == 0, height_sizes)))
        mean_height, mean_long = (height - sum(height_sizes)) / zero_y, (long - sum(long_sizes)) / zero_x
        x, y = door_sizes[0][0][0], door_sizes[0][0][1]
        for i in range(height_div):
            if height_sizes[i] == 0:
                y1 = y + mean_height
            else:
                y1 = y + height_sizes[i]
            for j in range(long_div):
                door_sizes[i][j][0] = x
                door_sizes[i][j][1] = y
                door_sizes[i][j][3] = y1
                if long_sizes[j] == 0:
                    x += mean_long
                    door_sizes[i][j][2] = x
                else:
                    x += long_sizes[j]
                    door_sizes[i][j][2] = x

            x, y = door_sizes[0][0][0], y1
        print(door_sizes)
        return door_sizes


"""
from PIL import Image, ImageDraw

height = 2500
long = 2500
doors = 1
divide = (
    (3, 2),
)
sizes = ((0, 400, 0), (0, 0))
doors_sizes = Ceil.get_sizes(height, long, doors, divide)

k = 0.15

doors_sizes[0] = Ceil.change_sizes(doors_sizes[0], divide[0], sizes, height, long)
print(*doors_sizes[0], sep='\n')

im = Image.new('RGB', (600, 600), (255, 255, 255))
draw = ImageDraw.Draw(im)

for door in doors_sizes:
    for col in door:
        for ceil in col:
            ceil = tuple(map(lambda elem: round(elem * k), ceil))
            draw.rectangle(ceil, outline=(0, 0, 0))

im.save('img.jpg', quality=95)
"""