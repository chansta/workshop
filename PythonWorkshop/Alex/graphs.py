T = len(profit_list)
varline = [varloss]*T
plt.subplot(3,1,1)
plt.plot(profit_list, "b", varline, "r")
plt.subplot(3,1,2)
plt.plot(loss_list)
plt.subplot(3,1,3)
plt.plot(accum_profit, "g", m_cp.data[0].transpose(), "black")
plt.show()
