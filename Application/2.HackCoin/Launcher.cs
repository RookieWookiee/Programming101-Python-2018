namespace HackBulgariaHackCoin
{
    using System;
    using System.Linq;

    /// <summary>
    /// Author: Yavor Lulchev, Skype: yavorlulchev
    /// </summary>
    class Launcher
    {
        static void Main()
        {
            var money = double.Parse(Console.ReadLine());
            var coins = 0.0;
            var stockPrices = Console.ReadLine()
                .Split(", ", StringSplitOptions.RemoveEmptyEntries)
                .Select(double.Parse)
                .ToArray();


            var inflectionMap = BuildInflectionMap(stockPrices);
            var stockStrategy = new string[stockPrices.Length];

            var currTrend = inflectionMap[0];

            for(int i = 1; i < inflectionMap.Length; i++) {
                if(inflectionMap[i] != currTrend) {
                    //local extremum found
                    if(currTrend == -1 && inflectionMap[i] == 1) {
                        //local minimum => buy
                        if(money > 0) {
                            //potential precision problems, divide by zero
                            coins += money / stockPrices[i-1];
                            money = 0;
                            stockStrategy[i-1] = "buy";
                        } else {
                            stockStrategy[i-1] = "hold";
                        }
                    } else {
                        //local maximum => sell
                        if(coins > 0) {
                            money = coins * stockPrices[i - 1];
                            coins = 0;
                            stockStrategy[i-1] = "sell";
                        } else {
                            stockStrategy[i-1] = "hold";
                        }
                    }
                    currTrend = inflectionMap[i];
                } else {
                    //no change => hold
                    stockStrategy[i-1] = "hold";
                }
            }

            Console.WriteLine((Math.Truncate(money * 100) / 100).ToString("F2"));
            Console.WriteLine(string.Join(", ", stockStrategy));
        }


        ///<summary>
        ///Returns a *new* array with *array*.Length+1 elements.
        ///The possible values within the result array are +1 and -1.
        ///-1 means that the previous item in *array* was bigger
        ///(descending trend).
        ///+1 means that the previous item in *array* was smaller
        ///(ascending trend).
        ///The element at index 0 will always be the complement
        ///of the element at index 1.
        ///The last element will always be -1.
        ///</summary>
        static double[] BuildInflectionMap(double[] array)
        {
            double[] map = new double[array.Length+1];
            for(int i = 1; i < array.Length; i++) {
                map[i] = (array[i] - array[i-1]) / Math.Abs(array[i] - array[i-1]);
            }

            map[map.Length-1] = -1;
            //Create an initial extremum.
            map[0] = map[1] * -1;
            return map;
        }
    }
}
