namespace HackBulgariaConnectedBombs
{
    using System;
    using System.Linq;
    using System.Collections.Generic;

    /// <summary>
    /// Author: Yavor Lulchev, Skype: yavorlulchev
    /// </summary>
    class Launcher
    {
        const string BombTypes = "RGB";

        const char VisitedSquare = '*';

        static void Main()
        {
            var bombs = ReadMatrix();
            var numClicks = GetNumberOfConnectedComponents(bombs);
            Console.WriteLine(numClicks);
        }

        private static int GetNumberOfConnectedComponents(char[][] bombs)
        {
            int count = 0;
            for(int i = 0; i < bombs.Length; i++) {
                for(int j = 0; j < bombs[i].Length; j++) {
                    if(BombTypes.Contains(bombs[i][j])) {
                        count++;
                        //Mark component
                        BFS(bombs, i, j, x => {
                            bombs[x.row][x.col] = VisitedSquare;
                        });
                    }
                }
            }

            return count;
        }

        private static void BFS(char[][] bombs, int startRow, int startCol, Action<(int row, int col)> action)
        {
            var queue = new Queue<(int row, int col)>();
            var bombType = bombs[startRow][startCol];

            queue.Enqueue((startRow, startCol));
            while(queue.Count > 0) {
                var currPos = queue.Dequeue();
                var neighbours = GetNeighbours(bombs, currPos, bombType);
                foreach(var neighbourPos in neighbours) {
                    action(neighbourPos);
                    queue.Enqueue(neighbourPos);
                }
            }
        }

        private static List<(int row, int col)> GetNeighbours(char[][] bombs, (int row, int col) startPos, char bombType)
        {
            var neighbours = new List<(int row, int col)>();
            int atRow = startPos.row,
                atCol = startPos.col;

            //clockwise
            var possiblePositions = new (int row, int col)[] {
                    (atRow-1, atCol+1), (atRow, atCol+1),   (atRow+1, atCol+1), (atRow+1, atCol-1),
                    (atRow+1, atCol),   (atRow+1, atCol-1), (atRow, atCol-1),   (atRow-1, atCol-1)
            };

            foreach(var pos in possiblePositions) {
                if(bombs.IsInBounds(pos.row, pos.col) && bombs[pos.row][pos.col] == bombType)
                    neighbours.Add(pos);
            }

            return neighbours;
        }

        static char[][] ReadMatrix()
        {
            var line = "";
            var input = new List<char[]>();
            while((line = Console.ReadLine()) != null && line != "") {
                input.Add(line.ToCharArray());
            }

            return input.ToArray();
        }
    }

    static class Extender
    {
        public static bool IsInBounds(this char[][] source, int row, int col)
        {
            if(row < 0 || row >= source.Length)
                return false;
            if(col < 0 || col >= source[row].Length)
                return false;
            return true;
        }
    }
}
