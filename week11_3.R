# %%
setwd("/Users/wtsama/Documents/code/code2/R/data/2assignment/")
library(openxlsx)
SZSE <- read.xlsx("399001_19_22.xlsx")
head(SZSE)
close <- SZSE$收盘价
date <- SZSE$交易时间
class(date)
# %%
# 将日期转换为日期对象(不知道为什么反正这个origin 相差 119 年少 2 天)
time <- as.Date(date, origin = as.Date("1899-12-30"))
df <- data.frame(time, close)
# 计算移动平均
library(TTR)
df$short_MA <- SMA(close, n = 10) # 10日短期均线
df$long_MA <- SMA(close, n = 60) # 60日长期均线

# %%
# 绘制价格走势图
library(ggplot2)
ggplot(df, aes(x = time, y = close)) +
  geom_line(color = "red", linewidth = 1) +
  geom_line(aes(y = short_MA), color = "grey", size = 1) +
  geom_line(aes(y = long_MA), color = "black", size = 1) +
  labs(title = "399001 Index Price Trend", x = "Date", y = "Close Price")

# %%
# 计算黄金交叉和死亡交叉点对应的横坐标以确定牛市和熊市、震荡股市的时间段
df$cross_point <- ifelse(df$short_MA > df$long_MA, "golden", "death")
class(df$cross_point)
df$RSI <- RSI(df$close, n = 14) # 获取相对强弱指数，14 个交易日
# 获取各自对应的时间
golden_cross_points <- which(df$cross_point == "golden")
death_cross_points <- which(df$cross_point == "death")
# 在df时间time列中获取对应的时间
golden_cross_times <- df$time[golden_cross_points]
death_cross_times <- df$time[death_cross_points]
# 震荡市时间获取
rsi_cross_points <- which(df$RSI > 70 | df$RSI < 30)
rsi_cross_times <- df$time[rsi_cross_points]
# 根据时间是否连续获取连续的时间段
golden_cross_periods <- rle(df$cross_point == "golden")
death_cross_periods <- rle(df$cross_point == "death")

# %%
# 将股市数据分市场类型整理成数据框
df_bull_market <- data.frame(
  golden_cross_times,
  df$close[golden_cross_points]
)
df_bear_market <- data.frame(
  death_cross_times,
  df$close[death_cross_points]
)
df_volatile_market <- data.frame(
  rsi_cross_times,
  df$close[rsi_cross_points]
)
# %%
# 计算收益率
return_bull <- diff(df_bull_market$df.close.golden_cross_points.) / df_bull_market$df.close.golden_cross_points.[-nrow(df_bull_market)]
return_bear <- diff(df_bear_market$df.close.death_cross_points.) / df_bear_market$df.close.death_cross_points.[-nrow(df_bear_market)]
return_volatile <- diff(df_volatile_market$df.close.rsi_cross_points.) / df_volatile_market$df.close.rsi_cross_points.[-nrow(df_volatile_market)]
# 新加一行数据到 return_xxxx
return_bull <- c(0, return_bull)
return_bear <- c(0, return_bear)
return_volatile <- c(0, return_volatile)
# 计算元素个数 length(return_bear)
df_bull_market$return <- return_bull
df_bear_market$return <- return_bear
df_volatile_market$return <- return_volatile
# 添加市场类型
df_bull_market$market <- "bull"
df_bear_market$market <- "bear"
df_volatile_market$market <- "volatile"
# 重命名列名
colnames(df_bull_market) <- c("date", "close", "return", "market")
colnames(df_bear_market) <- c("date", "close", "return", "market")
colnames(df_volatile_market) <- c("date", "close", "return", "market")
# 合并
df_all <- rbind(df_bull_market, df_bear_market, df_volatile_market)
head(df_all)
# %%
# 生成描述性统计结果
library(moments)
class(head(df_bull_market$return))
summary(df_bull_market$return)

skw_bull <- skewness(df_bull_market$return)
skw_bear <- skewness(df_bear_market$return)
skw_volatile <- skewness(df_volatile_market$return)
skw_res <- data.frame(
                      skewness = c(skw_bull, skw_bear, skw_volatile),
                      category = c("bull", "bear", "volatile"))

kurtosi_res <- data.frame(
  category = c("bull", "bear", "volatile"),
  kurtosis = sapply(list(
    df_bull_market$return,
    df_bear_market$return,
    df_volatile_market$return
  ), kurtosis)
)
as.list(skw_res)
as.list(kurtosi_res)

# %%
# 绘图
library(ggplot2)
# 绘图-在新的窗口
# quartz()
# options(device = "quartz")
ggplot(df_all, aes(x = date, y = close, color = market)) +
  geom_line(size = 1) +
  scale_color_manual(
    values = c("bull" = "#ede671", "bear" = "#8f8f8f", "volatile" = "#8377de"),
    labels = c("Bull Market", "Bear Market", "Volatile Market"),
    name = "Market Type"
  ) +
  labs(title = "Close Price Trends by Market Type", x = "Date", y = "Price") +
  theme_minimal()
  #ylim(-0.1, 0.1)  # 可选：限制Y轴范围便于观察波动
