if(!empty(prop("Recur Interval")) and !empty(prop("Due")),
    if(prop("Recur Interval") > 0 and prop("Recur Interval") == ceil(prop("Recur Interval")),
        lets(
            debug, false,
            
            recurUnit, ifs(
                prop("Recur Unit") == "Day(s)", "days",
                prop("Recur Unit") == "Week(s)", "weeks",
                prop("Recur Unit") == "Month(s)", "months",
                prop("Recur Unit") == "Year(s)", "years",
                prop("Recur Unit") == "Month(s) on the Last Day", "monthsonthelastday",
                prop("Recur Unit") == "Month(s) on the First Weekday", "monthsonthefirstweekday",
                prop("Recur Unit") == "Month(s) on the Last Weekday", "monthsonthelastweekday",
                "days"
            ),
            
            weekdays, match([
                if(
                    includes(prop("Recur week days"), "Monday"), 1, false
                ),
                
                if(
                    includes(prop("Recur week days"), "Tuesday"), 2, false
                ),
                
                if(
                    includes(prop("Recur week days"), "Wednesday"), 3, false
                ),
                
                if(
                    includes(prop("Recur week days"), "Thursday"), 4, false
                ),
                
                if(
                    includes(prop("Recur week days"), "Friday"), 5, false
                ),
                
                if(
                    includes(prop("Recur week days"), "Saturday"), 6, false
                ),
                
                if(
                    includes(prop("Recur week days"), "Sunday"), 7, false
                )
            ], "[1-7]"),
            
            dateDue, parseDate(formatDate(prop("Due"), "YYYY-MM-DD")),
            
            dateDueEnd, parseDate(formatDate(dateEnd(prop("Due")), "YYYY-MM-DD")),
            
            timeNow, now(),

            utcOffset, 2,
            
            offsetTimeNow, dateAdd(timeNow, utcOffset, "hours"),

            inUTC, if(formatDate(now(), "ZZ") == "+0000", true, false),
            
            hasValidOffset, if(!empty(utcOffset) and utcOffset >= -12 and utcOffset <= 14, true, false),
            
            hasRange, dateEnd(dateDueEnd) > dateStart(dateDue),
            
            dueRange, dateBetween(dateDueEnd, dateDue, "days"),
            
            conditionalTimeNow, if(inUTC and hasValidOffset, offsetTimeNow, timeNow),
            
            conditionalDateNow, parseDate(formatDate(conditionalTimeNow, "YYYY-MM-DD")),
            
            recurUnitLapseLength, if(includes(["days", "weeks", "months", "years"], recurUnit), dateBetween(conditionalDateNow, dateDue, recurUnit) / prop("Recur Interval"), false),
            
            lastDayBaseDate, if(
                includes(["monthsonthelastday", "monthsonthefirstweekday", "monthsonthelastweekday"], recurUnit),
                if(year(conditionalDateNow) * 12 + month(conditionalDateNow) - (year(dateDue) * 12 + month(dateDue)) > 0,
                    dateSubtract(dateAdd(dateSubtract(dateAdd(dateDue, ceil((year(conditionalDateNow) * 12 + month(conditionalDateNow) - (year(dateDue) * 12 + month(dateDue))) / prop("Recur Interval")) * prop("Recur Interval"), "months"), date(dateAdd(dateDue, ceil((year(conditionalDateNow) * 12 + month(conditionalDateNow) - (year(dateDue) * 12 + month(dateDue))) / prop("Recur Interval")) * prop("Recur Interval"), "months")) - 1, "days"), 1, "months"), 1, "days"),
                    dateSubtract(dateAdd(dateSubtract(dateAdd(dateDue, prop("Recur Interval"), "months"), date(dateAdd(dateDue, prop("Recur Interval"), "months")) - 1, "days"), 1, "months"), 1, "days")),
                false
            ),
            
            firstDayBaseDate, if(lastDayBaseDate != false, dateSubtract(lastDayBaseDate, date(lastDayBaseDate) - 1, "days"), false),
            
            firstWeekdayBaseDate, if(lastDayBaseDate != false,
                if(
                    test(day(firstDayBaseDate), "6|7"), 
                    dateAdd(firstDayBaseDate, 8 - day(firstDayBaseDate), "days"),
                    firstDayBaseDate
                ),
                false
            ),
            
            lastWeekdayBaseDate, if(lastDayBaseDate != false,
                if(
                    test(day(lastDayBaseDate), "6|7"), 
                    dateSubtract(lastDayBaseDate, day(lastDayBaseDate) - 5, "days"),
                    lastDayBaseDate
                ),
                false
            ),
            
            nextLastBaseDate, if(lastDayBaseDate != false,
                dateSubtract(dateAdd(dateSubtract(dateAdd(lastDayBaseDate, prop("Recur Interval"), "months"), date(dateAdd(lastDayBaseDate, prop("Recur Interval"), "months")) - 1, "days"), 1, "months"), 1, "days"),
                false
            ),
            
            nextFirstBaseDate, if(lastDayBaseDate != false, dateSubtract(nextLastBaseDate, date(nextLastBaseDate) - 1, "days"), false),
            
            nextFirstWeekday, if(lastDayBaseDate != false,
                if(
                    test(day(nextFirstBaseDate), "6|7"), 
                    dateAdd(nextFirstBaseDate, 8 - day(nextFirstBaseDate), "days"),
                    nextFirstBaseDate
                ),
                false
            ),
            
            nextLastWeekday, if(lastDayBaseDate != false,
                if(
                    test(day(nextLastBaseDate), "6|7"), 
                    dateSubtract(nextLastBaseDate, day(nextLastBaseDate) - 5, "days"),
                    nextLastBaseDate
                ),
                false
            ),
            
            nextDueStart, ifs(
                recurUnit == "days" and length(weekdays) > 0 and prop("Recur Interval") == 1, 
                    if(conditionalDateNow >= dateDue,
                        ifs(
                            includes(weekdays, format(day(dateAdd(conditionalDateNow, 1, "days")))), dateAdd(conditionalDateNow, 1, "days"),
                            includes(weekdays, format(day(dateAdd(conditionalDateNow, 2, "days")))), dateAdd(conditionalDateNow, 2, "days"),
                            includes(weekdays, format(day(dateAdd(conditionalDateNow, 3, "days")))), dateAdd(conditionalDateNow, 3, "days"),
                            includes(weekdays, format(day(dateAdd(conditionalDateNow, 4, "days")))), dateAdd(conditionalDateNow, 4, "days"),
                            includes(weekdays, format(day(dateAdd(conditionalDateNow, 5, "days")))), dateAdd(conditionalDateNow, 5, "days"),
                            includes(weekdays, format(day(dateAdd(conditionalDateNow, 6, "days")))), dateAdd(conditionalDateNow, 6, "days"),
                            includes(weekdays, format(day(dateAdd(conditionalDateNow, 7, "days")))), dateAdd(conditionalDateNow, 7, "days"),
                            false
                        ),
                        ifs(
                            includes(weekdays, format(day(dateAdd(dateDue, 1, "days")))), dateAdd(dateDue, 1, "days"),
                            includes(weekdays, format(day(dateAdd(dateDue, 2, "days")))), dateAdd(dateDue, 2, "days"),
                            includes(weekdays, format(day(dateAdd(dateDue, 3, "days")))), dateAdd(dateDue, 3, "days"),
                            includes(weekdays, format(day(dateAdd(dateDue, 4, "days")))), dateAdd(dateDue, 4, "days"),
                            includes(weekdays, format(day(dateAdd(dateDue, 5, "days")))), dateAdd(dateDue, 5, "days"),
                            includes(weekdays, format(day(dateAdd(dateDue, 6, "days")))), dateAdd(dateDue, 6, "days"),
                            includes(weekdays, format(day(dateAdd(dateDue, 7, "days")))), dateAdd(dateDue, 7, "days"),
                            false
                        )
                    ),
                
                recurUnit == "monthsonthelastday", if(conditionalDateNow >= lastDayBaseDate, nextLastBaseDate, lastDayBaseDate),
                
                recurUnit == "monthsonthefirstweekday", if(conditionalDateNow >= firstWeekdayBaseDate, nextFirstWeekday, firstWeekdayBaseDate),
                
                recurUnit == "monthsonthelastweekday", if(conditionalDateNow >= lastWeekdayBaseDate, nextLastWeekday, lastWeekdayBaseDate),
                
                includes(["days", "weeks", "months", "years"], recurUnit), 
                    if(dateBetween(conditionalDateNow, dateDue, "days") >= 1,
                        if(recurUnitLapseLength == ceil(recurUnitLapseLength),
                            dateAdd(dateDue, (recurUnitLapseLength + 1) * prop("Recur Interval"), recurUnit),
                            dateAdd(dateDue, ceil(recurUnitLapseLength) * prop("Recur Interval"), recurUnit)
                        ),
                        dateAdd(dateDue, prop("Recur Interval"), recurUnit)
                    ),
                false
            ),
            
            nextDueEnd, if(hasRange and nextDueStart != false, 
                dateAdd(nextDueStart, dueRange, "days"),
                false
            ),
            
            nextDue, if(hasRange and nextDueEnd != false, dateRange(nextDueStart, nextDueEnd), nextDueStart),
            
            if(
                debug == true,
                "---------\n" + prop("Task") + "\n---------" +
                "\npropDue: " + prop("Due") +
                "\npropRecurInterval: " + prop("Recur Interval") +
                "\npropRecurUnit: " + prop("Recur Unit") +
                "\npropDays: " + prop("Recur week days") +
                "\npropUTCOffset: " + utcOffset +
                "\nrecurUnit: " + recurUnit +
                "\nweekdays: " + weekdays +
                "\ndateDue: " + dateDue +
                "\ndateDueEnd: " + dateDueEnd +
                "\ntimeNow: " + timeNow +
                "\noffsetTimeNow: " + offsetTimeNow +
                "\ninUTC: " + inUTC +
                "\nhasValidOffset: " + hasValidOffset +
                "\nhasRange: " + hasRange +
                "\ndueRange: " + dueRange +
                "\nconditionalTimeNow: " + conditionalTimeNow +
                "\nconditionalDateNow: " + conditionalDateNow +
                "\nrecurUnitLapseLength: " + recurUnitLapseLength +
                "\nlastDayBaseDate: " + lastDayBaseDate +
                "\nfirstDayBaseDate: " + firstDayBaseDate +
                "\nfirstWeekdayBaseDate: " + firstWeekdayBaseDate +
                "\nlastWeekdayBaseDate: " + lastWeekdayBaseDate +
                "\nnextLastBaseDate: " + nextLastBaseDate +
                "\nnextFirstBaseDate: " + nextFirstBaseDate +
                "\nnextFirstWeekday: " + nextFirstWeekday +
                "\nnextLastWeekday: " + nextLastWeekday +
                "\nnextDueStart: " + nextDueStart +
                "\nnextDueEnd: " + nextDueEnd +
                "\nnextDue: " + nextDue,
                nextDue
            )
        ),
    "Error: Non-Whole or Negative Recur Interval"),
"")
