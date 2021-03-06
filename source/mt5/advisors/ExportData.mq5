//+------------------------------------------------------------------+
//|                                                  Export Data.mq5 |
//|                                  Copyright 2022, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2022, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"

input bool SendToFTP;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create timer
   EventSetTimer(10);
   Print("Init");
   ExportQuotes();
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();

  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   Print("OnTick");
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//---
   Print("OnTimer");
  }
//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
  {
//---
   Print("OnChartEvent");
  }
//+------------------------------------------------------------------+

void ExportQuotes()
{
   Print("go exp");
   string fileName = Symbol() + "_D1" + ".csv";
   if (FileIsExist(fileName))
   {
      FileDelete(fileName);
   }
   int hFl=FileOpen(fileName,FILE_WRITE|FILE_CSV|FILE_ANSI,',');
   FileWrite(hFl,"date_time","open","low","high","close","vol");
   for(int i = iBars(Symbol(),Period())-10; i >= 0; i--)
   {
      FileWrite(hFl,
                   iTime(Symbol(),Period(),i),        // Дата-время
                   iOpen(Symbol(),Period(),i),        // Цена открытия
                   iLow(Symbol(),Period(),i),         // Цена минимума
                   iHigh(Symbol(),Period(),i),        // Цена максимума
                   iClose(Symbol(),Period(),i),       // Цена закрытия
                   iVolume(Symbol(),Period(),i));     // Цена тикового объёма
   }
   FileClose(hFl);
   if (SendToFTP)
   {
      Print(fileName);
      bool res = SendFTP(fileName);
      Print("Send to FTP: ", res);
      if (!res)
      {
         Alert("FTP: ",GetLastError());
      }
   }
   Print("end exp");
}

//+------------------------------------------------------------------+