import logging
import config

from datetime import datetime
from telegram.ext import Updater, CommandHandler
from telegram.parsemode import ParseMode

from statistics import retrieve_latest_cases_stats

from statistics_record import StatisticsRecord

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)
LATEST_STATS: StatisticsRecord = None


def start_handler(update, context):
    """Returns a basic welcome message on /start"""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Estatísticas COVID em Portugal",
    )


def stats_handler(update, context):
    """Generates the latest stats data response and sends it to TG"""
    response = generate_response()
    dispatch_response(context, response, update)


def generate_response():
    record: StatisticsRecord = get_cases_data()
    if not record:
        response = "Sem dados actualmente..."
    else:
        people_vaccinated_per_hundred = record.people_vaccinated_per_hundred
        people_fully_vaccinated_per_hundred = record.people_fully_vaccinated_per_hundred
        boosters_per_hundred = record.total_boosters_per_hundred

        one_vax_progress = "".join(
            "■" * int(people_vaccinated_per_hundred / 10)
        ) + "".join("□" * int((100 - people_vaccinated_per_hundred) / 10))

        two_vax_progress = "".join(
            "■" * int(people_fully_vaccinated_per_hundred / 10)
        ) + "".join("□" * int((100 - people_fully_vaccinated_per_hundred) / 10))

        booster_vax_progress = "".join("■" * int(boosters_per_hundred / 10)) + "".join(
            "□" * int((100 - boosters_per_hundred) / 10)
        )

        response = (
                "\n"
                + "*Estatísticas Vacinação Portugal em {}*\n"
                + "`População com primeira dose apenas: {} {}%`\n"
                + "`População com vacinação completa:   {} {}%`\n"
                + "`População com vacinação de reforço: {} {}%`\n"
                + "\n"
                + "`Há {:0.0f} novos casos e {:0.0f} óbitos.`\n"
                + "`Encontram-se {:0.0f} pacientes hospitalizados dos quais {:0.0f} em UCI.`\n"
                + "\n"
                # + "`A taxa de positividade é {:.1%}. R₀ = {:0.2f}`\n"
                + "`R₀ = {:0.2f}`\n"
        ).format(
            record.last_updated_date.replace("-", "/"),
            one_vax_progress,
            people_vaccinated_per_hundred,
            two_vax_progress,
            people_fully_vaccinated_per_hundred,
            booster_vax_progress,
            boosters_per_hundred,
            record.new_cases,
            record.new_deaths,
            record.hosp_patients,
            record.icu_patients,
            #  0 if record.positive_rate == None else record.positive_rate,
            record.reproduction_rate,
        )
    return response


def dispatch_response(context, response, update):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


def get_cases_data() -> StatisticsRecord:
    """Retrieves the latest cases data. Reuses cached data if possible."""
    global LATEST_STATS

    current_date = datetime.now().date()

    if LATEST_STATS:
        latest_date_available = datetime.strptime(
            LATEST_STATS.last_updated_date, "%Y-%m-%d"
        ).date()

        if latest_date_available == current_date:
            log.info("Reusing cached dataset for " + str(latest_date_available))
            return LATEST_STATS

    log.info("Retrieving datasets from OWID.")
    LATEST_STATS = retrieve_latest_cases_stats()
    return LATEST_STATS


def main():
    updater = Updater(config.TG_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", stats_handler))
    dp.add_handler(CommandHandler("stats", stats_handler))

    log.info("Starting....")

    updater.start_webhook(
        listen="0.0.0.0",
        port=config.WEB_HOOK_PORT,
        url_path=config.TG_TOKEN,
        webhook_url=config.WEB_HOOK_URL + config.TG_TOKEN,
    )

    updater.idle()


if __name__ == "__main__":
    main()
