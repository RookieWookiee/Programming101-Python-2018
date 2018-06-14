namespace HackBulgariaBalanceCalculation
{
    using System;
    using System.Collections.Generic;
    using System.Globalization;
    using System.Linq;

    /// <summary>
    /// Author: Yavor Lulchev, Skype: yavorlulchev
    /// !This program is by no means fault tolerant.!
    /// </summary>
    class Launcher
    {
        static void Main()
        {
            var line = "";
            var transactionsByDate = new SortedDictionary<DateTime, double>();

            while ((line = Console.ReadLine().Trim()) != "----") {
                var tokens = line.Split(',');
                var transactionAmount = double.Parse(tokens[0]);
                var date = DateTime.ParseExact(tokens[1], @"dd/MM/yyyy", CultureInfo.InvariantCulture);

                if (!transactionsByDate.ContainsKey(date))
                    transactionsByDate[date] = 0.0;

                transactionsByDate[date] += transactionAmount;
            }

            var endDateString = Console.ReadLine().Trim();
            var endDate = DateTime.ParseExact(endDateString, @"dd/MM/yyyy", CultureInfo.InvariantCulture);

            double totalAmount = GetTotalAmountUntilDate(transactionsByDate, endDate);

            var plusSign = totalAmount > 0 ? "+" : "";

            Console.WriteLine($"{plusSign}{totalAmount}");
        }

        private static double GetTotalAmountUntilDate(SortedDictionary<DateTime, double> transactionsByDate, DateTime endDate)
        {
            var totalAmount = 0.0;

            foreach (var transactionDateKvp in transactionsByDate) {
                var currDate = transactionDateKvp.Key;
                var currAmount = transactionDateKvp.Value;
                if (currDate.CompareTo(endDate) <= 0)
                    totalAmount += currAmount;
                else
                    break;
            }

            return totalAmount;
        }
    }
}
