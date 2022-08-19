import pandas as pd
EMPTY = None

board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

print(pd.DataFrame(enumerate(board))[0])