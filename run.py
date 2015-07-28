import crud
import getStockData as gsd


datacfg = gsd.getconfig()
dbcfg = crud.getDbConfig()
a = gsd.getresult(gsd.getrawdata(datacfg,gsd.geturl(datacfg)[0]))
crud.batchInsert(dbcfg,'tbl_stock_code',a)