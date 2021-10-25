add_function("set", function (arguments)
    set_db(arguments.key, arguments.value)
end)

add_function("get", function (arguments)
    return get_db(arguments)
end)