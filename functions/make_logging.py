class make_logging(object):
    def log_info(self,content:str,type='info'):
        """
        desc: write log content to file
        """
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)  # Log等级总开关

        # 创建一个filehandler，用于写入日志文件
        os.path.join(os.path.dirname(os.getcwd()))
        file_path=os.path.split(sys.argv[0])[1] + "_" + str(datetime.date.today()) + ".log"
        logfile = os.path.join(file_path)
        fh = logging.FileHandler(logfile, mode='a')
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("{} - %(asctime)s - %(levelname)s: %(message)s".format(os.path.split(sys.argv[0])[1]))
        fh.setFormatter(formatter)

        # 第四步，将logger添加到handler里面
        logger.addHandler(fh)
        if type=="debug":logger.debug(content)
        elif type=="info":logger.info(content)
        elif type=="warning":logger.warning(content)
        elif type=="error":logger.error(content)

if __name__ == '__main__':
    make_logging().log_info("write your logger content")