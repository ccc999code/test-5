import json
import os
import streamlit as st

FILE_NAME = "users.json"

# 設定網頁標題與圖示
st.set_page_config(page_title="文字修仙模擬器", page_icon="☯️", layout="centered")


# 讀取玩家資料
def load_users():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


# 儲存玩家資料
def save_users(users):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


# 根據等級判斷境界
def get_realm(level):
    if level >= 1151:
        return "游仙巔峰"
    elif level >= 1069:
        return "游仙後期"
    elif level >= 988:
        return "游仙中期"
    elif level >= 907:
        return "游仙初期"
    elif level >= 826:
        return "大乘巔峰"
    elif level >= 761:
        return "大乘後期"
    elif level >= 697:
        return "大乘中期"
    elif level >= 633:
        return "大乘初期"
    elif level >= 569:
        return "練虛巔峰"
    elif level >= 519:
        return "練虛後期"
    elif level >= 470:
        return "練虛中期"
    elif level >= 421:
        return "練虛初期"
    elif level >= 372:
        return "合體巔峰"
    elif level >= 335:
        return "合體後期"
    elif level >= 299:
        return "合體中期"
    elif level >= 263:
        return "合體初期"
    elif level >= 227:
        return "化神巔峰"
    elif level >= 201:
        return "化神後期"
    elif level >= 176:
        return "化神中期"
    elif level >= 151:
        return "化神初期"
    elif level >= 126:
        return "元嬰巔峰"
    elif level >= 109:
        return "元嬰後期"
    elif level >= 93:
        return "元嬰中期"
    elif level >= 77:
        return "元嬰初期"
    elif level >= 61:
        return "金丹巔峰"
    elif level >= 51:
        return "金丹後期"
    elif level >= 42:
        return "金丹中期"
    elif level >= 33:
        return "金丹初期"
    elif level >= 24:
        return "築基巔峰"
    elif level >= 19:
        return "築基後期"
    elif level >= 15:
        return "築基中期"
    elif level >= 11:
        return "築基初期"
    elif level >= 7:
        return "練氣巔峰"
    elif level >= 4:
        return "練氣後期"
    elif level >= 2:
        return "練氣中期"
    else:
        return "煉氣初期"


# 升級判斷
def check_level_up(player):
    # 支援連續升級
    leveled_up = False
    while player["exp"] >= 100:
        player["exp"] -= 100
        player["level"] += 1
        player["realm"] = get_realm(player["level"])
        leveled_up = True
    if leveled_up:
        st.balloons()  # 噴發慶祝氣球
        st.success(
            f"🎉 突破成功！你的等級提升到 **{player['level']}**，目前境界為：**{player['realm']}**"
        )


# 初始化 Session State (用於維持網頁登入狀態)
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

users = load_users()

# ==================== 主介面邏輯 ====================
st.title("☯️ 文字修仙模擬器")

# --- 未登入狀態 ---
if st.session_state.logged_in_user is None:
    tab1, tab2 = st.tabs(["🔐 登入帳號", "📝 註冊帳號"])

    with tab1:
        st.subheader("歡迎回到修仙世界")
        login_user = st.text_input("帳號", key="login_user")
        login_pwd = st.text_input("密碼", type="password", key="login_pwd")
        if st.button("確認登入", type="primary"):
            if login_user not in users:
                st.error("❌ 查無此帳號！")
            elif users[login_user]["password"] == login_pwd:
                st.session_state.logged_in_user = login_user
                st.rerun()
            else:
                st.error("❌ 密碼錯誤！")

    with tab2:
        st.subheader("踏上修仙之路")
        reg_user = st.text_input("請輸入要註冊的帳號", key="reg_user")
        reg_pwd = st.text_input("請輸入要註冊的密碼", type="password", key="reg_pwd")
        if st.button("確認註冊"):
            if not reg_user or not reg_pwd:
                st.warning("⚠️ 帳號或密碼不能為空！")
            elif reg_user in users:
                st.error("❌ 這個帳號已經存在了！")
            else:
                users[reg_user] = {
                    "password": reg_pwd,
                    "level": 1,
                    "exp": 0,
                    "money": 100,
                    "hp": 100,
                    "realm": "煉氣初期",
                }
                save_users(users)
                st.success("✨ 註冊成功！你已踏上修仙之路，請切換至登入頁面。")

# --- 已登入狀態 (修仙系統首頁) ---
else:
    current_user = st.session_state.logged_in_user
    player = users[current_user]

    # 側邊欄：顯示玩家基本資料與登出按鈕
    with st.sidebar:
        st.header(f"👤 道友：{current_user}")
        st.markdown(f"**當前境界：** `{player['realm']}`")
        st.markdown(f"**當前等級：** {player['level']}")

        # 進度條顯示經驗值
        st.write(f"經驗值: {player['exp']} / 100")
        st.progress(player["exp"] / 100)

        # 進度條顯示生命值
        st.write(f"生命值: {player['hp']} / 100")
        st.progress(player["hp"] / 100)

        st.markdown(f"**擁有靈石：** 💰 {player['money']}")

        st.write("---")
        if st.button("🚪 登出系統", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()

    # 主畫面功能分頁
    menu_tab1, menu_tab2, menu_tab3, menu_tab4 = st.tabs(
        ["🧘 洞府修煉", "⚔️ 外出歷練", "🛍️ 休息與簽到", "🏆 修仙排行榜"]
    )

    # 1. 洞府修煉
    with menu_tab1:
        st.subheader("🧘 閉關打坐")
        st.write("你在洞府內盤腿而坐，運轉功法，吸收天地靈氣……")
        if st.button("開始修煉 (經驗 +25)", type="primary"):
            player["exp"] += 25
            st.info("🧘 修煉完成！經驗值 +25")
            check_level_up(player)
            save_users(users)
            st.rerun()

    # 2. 外出歷練
    with menu_tab2:
        st.subheader("⚔️ 後山歷練")
        st.write("後山妖獸橫行，危險與機遇並存。歷練將消耗 20 生命值。")

        if player["hp"] <= 0:
            st.error("❌ 你目前生命值太低，無法外出歷練，請先休息恢復。")
        else:
            if st.button("前往後山歷練", type="secondary"):
                st.write("⚔️ 你與一隻低階妖獸展開了激烈的戰鬥……")
                player["hp"] -= 20
                player["exp"] += 30
                player["money"] += 50

                if player["hp"] < 0:
                    player["hp"] = 0

                st.success("🏆 戰鬥勝利！獲得：經驗值 +30、靈石 +50")
                st.warning("💥 受到傷害：生命值 -20")

                check_level_up(player)
                save_users(users)
                st.rerun()

    # 3. 休息與簽到
    with menu_tab3:
        st.subheader("📅 每日福利")
        if st.button("領取今日簽到獎勵"):
            player["money"] += 100
            save_users(users)
            st.success("💰 簽到成功！獲得靈石 100。")
            st.rerun()

        st.write("---")
        st.subheader("💤 仙客棧休息")
        st.write("花費 **30 靈石** 在客棧下榻，可將生命值完全恢復。")
        if st.button("花費 30 靈石休息"):
            if player["money"] < 30:
                st.error("❌ 你的靈石不足，無法休息恢復。")
            else:
                player["money"] -= 30
                player["hp"] = 100
                save_users(users)
                st.success("💖 休息完成！生命值已恢復到 100。")
                st.rerun()

    # 4. 排行榜
    with menu_tab4:
        st.subheader("🏆 天道榜（修仙排行榜）")
        if not users:
            st.write("目前沒有任何玩家資料。")
        else:
            sorted_users = sorted(
                users.items(), key=lambda item: item[1]["level"], reverse=True
            )

            # 建立美觀的網頁表格
            rank_data = []
            for index, (uname, data) in enumerate(sorted_users, start=1):
                rank_data.append(
                    {
                        "名次": index,
                        "道號": uname,
                        "等級": data["level"],
                        "境界": data["realm"],
                        "靈石": data["money"],
                    }
                )
            st.table(rank_data)
