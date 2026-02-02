"""
心理测试项目 - Selenium 自动化测试
测试内容：页面加载、题目显示、答题交互、提交、重置、换题
"""

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class TestPsychQuiz:
    """心理测试页面自动化测试类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置：启动浏览器"""
        chrome_options = Options()
        # 如果想看到浏览器界面，注释下面这行
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
        # 获取 index.html 的绝对路径
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.page_url = f"file:///{project_dir}/index.html".replace("\\", "/")
        
        yield
        
        # 测试后置：关闭浏览器
        self.driver.quit()

    def test_01_page_loads(self):
        """测试1：页面正常加载，标题正确"""
        self.driver.get(self.page_url)
        assert "心理测试" in self.driver.title
        
        # 检查页面大标题
        h1 = self.driver.find_element(By.TAG_NAME, "h1")
        assert "简易心理测试" in h1.text
        assert "10 题" in h1.text

    def test_02_questions_displayed(self):
        """测试2：页面显示 10 道题目"""
        self.driver.get(self.page_url)
        
        questions = self.driver.find_elements(By.CLASS_NAME, "question")
        assert len(questions) == 10, f"期望 10 道题，实际 {len(questions)} 道"
        
        # 每道题应有 4 个选项
        for i, q in enumerate(questions, 1):
            radios = q.find_elements(By.CSS_SELECTOR, "input[type='radio']")
            assert len(radios) == 4, f"第 {i} 题应有 4 个选项"

    def test_03_submit_button_disabled_initially(self):
        """测试3：未答题时提交按钮禁用"""
        self.driver.get(self.page_url)
        
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        assert submit_btn.get_attribute("disabled") is not None, "提交按钮应该是禁用状态"

    def test_04_submit_enabled_after_all_answered(self):
        """测试4：全部答完后提交按钮启用"""
        self.driver.get(self.page_url)
        
        # 给每道题选一个答案
        for i in range(1, 11):
            radio = self.driver.find_element(By.CSS_SELECTOR, f"input[name='q{i}'][value='2']")
            radio.click()
        
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        assert submit_btn.get_attribute("disabled") is None, "全部答完后提交按钮应该启用"

    def test_05_partial_answer_submit_disabled(self):
        """测试5：只答部分题目，提交按钮仍禁用"""
        self.driver.get(self.page_url)
        
        # 只答前 5 题
        for i in range(1, 6):
            radio = self.driver.find_element(By.CSS_SELECTOR, f"input[name='q{i}'][value='1']")
            radio.click()
        
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        assert submit_btn.get_attribute("disabled") is not None, "未答完时提交按钮应禁用"

    def test_06_submit_shows_result(self):
        """测试6：提交后显示结果"""
        self.driver.get(self.page_url)
        
        # 答所有题（选"不符合" = 0 分）
        for i in range(1, 11):
            radio = self.driver.find_element(By.CSS_SELECTOR, f"input[name='q{i}'][value='0']")
            radio.click()
        
        # 点击提交
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        submit_btn.click()
        
        # 等待结果区域显示
        result = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "result"))
        )
        
        score_text = self.driver.find_element(By.ID, "scoreText").text
        assert "得分" in score_text
        assert "0/30" in score_text  # 全选 0 分，总分 0/30
        assert "低" in score_text  # 低压力水平

    def test_07_high_score_result(self):
        """测试7：高分结果显示（较高压力）"""
        self.driver.get(self.page_url)
        
        # 答所有题（选"非常符合" = 3 分）
        for i in range(1, 11):
            radio = self.driver.find_element(By.CSS_SELECTOR, f"input[name='q{i}'][value='3']")
            radio.click()
        
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        submit_btn.click()
        
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "result"))
        )
        
        score_text = self.driver.find_element(By.ID, "scoreText").text
        assert "30/30" in score_text
        assert "较高" in score_text

    def test_08_medium_score_result(self):
        """测试8：中等分数结果"""
        self.driver.get(self.page_url)
        
        # 前 5 题选 3 分，后 5 题选 0 分 → 总分 15/30 = 50%
        for i in range(1, 6):
            radio = self.driver.find_element(By.CSS_SELECTOR, f"input[name='q{i}'][value='3']")
            radio.click()
        for i in range(6, 11):
            radio = self.driver.find_element(By.CSS_SELECTOR, f"input[name='q{i}'][value='0']")
            radio.click()
        
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        submit_btn.click()
        
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "result"))
        )
        
        score_text = self.driver.find_element(By.ID, "scoreText").text
        assert "15/30" in score_text
        assert "中等" in score_text

    def test_09_reset_button(self):
        """测试9：重置按钮清空答案和结果"""
        self.driver.get(self.page_url)
        
        # 先答题并提交
        for i in range(1, 11):
            radio = self.driver.find_element(By.CSS_SELECTOR, f"input[name='q{i}'][value='2']")
            radio.click()
        
        submit_btn = self.driver.find_element(By.ID, "submitBtn")
        submit_btn.click()
        
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "result"))
        )
        
        # 点击重置
        reset_btn = self.driver.find_element(By.ID, "resetBtn")
        reset_btn.click()
        
        # 结果区域应该隐藏
        result = self.driver.find_element(By.ID, "result")
        assert "hidden" in result.get_attribute("class"), "重置后结果应隐藏"
        
        # 提交按钮应禁用
        assert submit_btn.get_attribute("disabled") is not None, "重置后提交按钮应禁用"
        
        # 所有选项应取消选中
        checked = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']:checked")
        assert len(checked) == 0, "重置后不应有选中的选项"

    def test_10_reshuffle_button(self):
        """测试10：换一组题目按钮"""
        self.driver.get(self.page_url)
        
        # 记录当前题目的 data-qid
        questions_before = self.driver.find_elements(By.CLASS_NAME, "question")
        qids_before = [q.get_attribute("data-qid") for q in questions_before]
        
        # 点击换题（多试几次，因为有随机性）
        reshuffle_btn = self.driver.find_element(By.ID, "reshuffleBtn")
        
        changed = False
        for _ in range(5):  # 最多尝试 5 次
            reshuffle_btn.click()
            time.sleep(0.3)
            
            questions_after = self.driver.find_elements(By.CLASS_NAME, "question")
            qids_after = [q.get_attribute("data-qid") for q in questions_after]
            
            if qids_before != qids_after:
                changed = True
                break
        
        assert changed, "换题后题目应该改变（随机抽取）"

    def test_11_reshuffle_clears_answers(self):
        """测试11：换题后清空已选答案"""
        self.driver.get(self.page_url)
        
        # 先选几个答案
        for i in range(1, 6):
            radio = self.driver.find_element(By.CSS_SELECTOR, f"input[name='q{i}'][value='1']")
            radio.click()
        
        # 换题
        reshuffle_btn = self.driver.find_element(By.ID, "reshuffleBtn")
        reshuffle_btn.click()
        time.sleep(0.3)
        
        # 检查没有选中的选项
        checked = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']:checked")
        assert len(checked) == 0, "换题后不应有选中的选项"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
