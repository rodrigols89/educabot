#!/usr/bin/env bash

set -e

# ============================================================================
# Root directory
# ============================================================================

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

MAKE="make -C $ROOT --no-print-directory"

# ============================================================================
# Colors
# ============================================================================

GREEN="\033[1;32m"
DARK_GREEN="\033[0;32m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

# ============================================================================
# Layout
# ============================================================================

COL_WIDTH=38

print3() {
    printf " %-${COL_WIDTH}s %-${COL_WIDTH}s %s\n" "$1" "$2" "$3"
}

# ============================================================================

while true
do
    clear

    echo -e "${GREEN}"
    echo "┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐"
    echo "│                                              🚀 EDUCABOT v1.0                                                          │"
    echo "│                                   WhatsApp Orders Management Console                                                   │"
    echo "└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘"
    echo -e "${RESET}"

    ###########################################################################
    # Primeira linha
    ###########################################################################

    echo -e "${CYAN}🐳 Docker                               📜 Logs                                 ⚡ FastAPI${RESET}"
    print3 "──────────────────────────────" "──────────────────────────────" "──────────────────────────────"

    print3 "01) Start Containers"     "06) PostgreSQL Logs" "09) Start Server"
    print3 "02) Stop Containers"      "07) Redis Logs"      "10) Check Server"
    print3 "03) Restart Containers"   "08) Evolution Logs"  "11) Kill Server"
    print3 "04) Build Containers"     ""                    ""
    print3 "05) Clean Docker"         ""                    ""

    echo

    ###########################################################################
    # Segunda linha
    ###########################################################################

    echo -e "${CYAN}🗄  Database                             🧪 Development                          ⚙  Systemd${RESET}"
    print3 "──────────────────────────────" "──────────────────────────────" "──────────────────────────────"

    print3 "12) PostgreSQL Shell" "14) Lint"                "18) Init Project"
    print3 "13) Evolution Shell"  "15) Pre-commit"          "19) Init Service"
    print3 ""                     "16) Tests"               "20) Service Status"
    print3 ""                     "17) Export Requirements" "21) Restart Service"
    print3 ""                     ""                        "22) Stop Service"
    print3 ""                     ""                        "23) Service Logs"

    echo
    echo "──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"
    echo
    echo -e "                                            ${RED}0) Exit${RESET}"
    echo

    read -rp "$(echo -e "${YELLOW}Select an option ❯ ${RESET}")" OPTION

    echo

    case "$OPTION" in
        1)  $MAKE start_compose ;;
        2)  $MAKE down_compose ;;
        3)  $MAKE restart_compose ;;
        4)  $MAKE build_compose ;;
        5)  $MAKE clean_compose ;;

        6)  $MAKE log_postgres ;;
        7)  $MAKE log_redis ;;
        8)  $MAKE log_evolution ;;

        9)  $MAKE server ;;
        10) $MAKE check_server ;;
        11) $MAKE kill_server ;;

        12) $MAKE open_db ;;
        13) $MAKE open_evolution ;;

        14) $MAKE lint ;;
        15) $MAKE precommit ;;
        16) $MAKE test ;;
        17) $MAKE export_prod ;;

        18) $MAKE init_project ;;
        19) $MAKE init_service ;;
        20) $MAKE service_status ;;
        21) $MAKE service_restart ;;
        22) $MAKE service_stop ;;
        23) $MAKE service_logs ;;

        0)
            clear
            echo -e "${GREEN}👋 Goodbye!${RESET}"
            exit 0
            ;;

        *)
            echo -e "${RED}Invalid option!${RESET}"
            ;;
    esac

    echo
    echo -e "${DARK_GREEN}Press ENTER to return to the menu...${RESET}"
    read
done
