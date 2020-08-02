#include <iostream>
#include <algorithm>
#include <chrono>
#include <random>
#include <vector>
#include <map>
#include <set>

using namespace std;

set<char> valid_charset;
map<string, long long> vars;

mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

long long rnd_wnext(long long minw, long long maxw) {
    uniform_int_distribution<long long> wnext(minw, maxw);
    return wnext(rng);
}

/* preprocessing part */

string strip(string s) {
    string t = "";
    for (char ch : s) {
        if (valid_charset.count(ch)) {
            t += ch;
        }
    }
    return t;
}

pair<string, string> get_type_specs(string s) {
    string type = "";
    string specs = "";
    int n = (int) s.size(), i = 0;
    while (i < n && s[i] != '[') {
        type += s[i++];
    }
    if (i < n) {
        specs = s.substr(i);
    }
    return make_pair(type, specs);
}

vector<string> tokenizeProperty(string s) {
    vector<string> res;
    string t = "";
    for (int i = 1; i + 1 < s.size(); ++i) {
        char ch = s[i];
        if (ch == ':') {
            if (t == "") {
                res.clear(); break;
            }
            res.push_back(t);
            t = "";
        } else {
            t += ch;
        }
    }
    if (t == "") {
        res.clear();
        return res;
    }
    res.push_back(t);
    return res;
}

vector<string> tokenizeScript(string s) {
    vector<string> res;
    vector<int> idx;
    int n = (int) s.size();
    for (int i = 0; i < n; ++i) {
        if (s[i] == '>') {
            idx.push_back(i);
        }
    }
    for (int i = 0; i < n; ++i) {
        if (s[i] == '<') {
            auto ptr = upper_bound(idx.begin(), idx.end(), i);
            if (ptr == idx.end()) {
                return {"invalid_cmd"};
            }
            int j = *ptr;
            res.push_back(s.substr(i + 1, j - i - 1));
            i = j;
        } else {
            return {"invalid_cmd"};
        }
    }
    return res;
}

/* getter method part */

bool var_exists(string var) {
    return vars.count(var) > 0;
}

bool validVarName(string var) {
    if (var.size() < 2 || var[0] != '$' || (var[1] != '_' && !isalpha(var[1]))) {
        return false;
    }
    return true;
}

bool isVar(string var) {
    return validVarName(var) && var_exists(var);
}

bool isInt(string var) {
    int from = (var[0] == '-');
    for (int i = from; i < var.size(); ++i) {
        if (!isdigit(var[i])) {
            return false;
        }
    }
    return true;
}

bool isBool(string var) {
    return var == "0" || var == "1";
}

bool isEndWith(string var) {
    return var == "line" || var == "space";
}

bool isVarParam(string var) {
    return isVar(var) || isInt(var);
}

bool isCharNotation(string spec) {
    int n = (int) spec.size();
    if (!n || (n != 3 && n != 6 && n != 9)) {
        return false;
    }
    for (int i = 0; i < n; i += 3) {
        string notation = "";
        notation += spec[i];
        notation += spec[i + 1];
        notation += spec[i + 2];
        if (notation != "a-z" && notation != "A-Z" && notation != "0-9") {
            return false;
        }
    }
    return true;
}

long long var_value(string var) {
    if (isVar(var)) {
        return vars[var];
    }
    return stol(var);
}


/* Validation part of the params*/

string validate_var(string var, string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    if (!validVarName(var)) {
        return ": variable name is not valid";
    }
    if (var_exists(var)) {
        return ": " + var + " is re-declared.";
    }
    vector<string> tokens = tokenizeProperty(specs);
    if (tokens.size() != 2) {
        return ": parameters are not correct.";
    }
    if (!isVarParam(tokens[0]) || !isVarParam(tokens[1])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) > var_value(tokens[1])) {
        return ": min_value, max_value are not correct.";
    }
    vars[var] = rnd_wnext(var_value(tokens[0]), var_value(tokens[1]));
    return "";
}

string validate_int_array(string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    vector<string> tokens = tokenizeProperty(specs);

    if (tokens.size() != 5) {
        return ": parameters are not correct.";
    }
    if (!isVarParam(tokens[0]) || !isVarParam(tokens[1]) || !isVarParam(tokens[2])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) < 1) {
        return ": array size should be positive.";
    }
    if (var_value(tokens[1]) > var_value(tokens[2])) {
        return ": min_value, max_value are not correct.";
    }
    if (!isBool(tokens[3]) || !isEndWith(tokens[4])) {
        return ": parameters are not correct.";
    }

    return "";
}

string validate_int_pair(string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    vector<string> tokens = tokenizeProperty(specs);

    if (tokens.size() != 4) {
        return ": parameters are not correct.";
    }
    if (!isVarParam(tokens[0]) || !isVarParam(tokens[1]) || !isVarParam(tokens[2]) || !isBool(tokens[3])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) < 1) {
        return ": pair size should be positive.";
    }
    if (var_value(tokens[1]) > var_value(tokens[2])) {
        return ": min_value, max_value are not correct.";
    }

    return "";
}

string validate_int_permutation(string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    vector<string> tokens = tokenizeProperty(specs);

    if (tokens.size() != 2) {
        return ": parameters are not correct.";
    }
    if (!isVarParam(tokens[0]) || !isBool(tokens[1])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) < 1) {
        return ": permutation size should be positive.";
    }

    return "";
}

string validate_tree(string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    vector<string> tokens = tokenizeProperty(specs);
    if (tokens.size() != 1 || !isVarParam(tokens[0])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) < 1) {
        return ": number of node should be positive.";
    }
    return "";
}

string validate_weighted_tree(string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    vector<string> tokens = tokenizeProperty(specs);
    if (tokens.size() != 3 || !isVarParam(tokens[0]) || !isVarParam(tokens[1]) || !isVarParam(tokens[2])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) < 1) {
        return ": number of node should be positive.";
    }
    if (var_value(tokens[1]) > var_value(tokens[2])) {
        return ": min_value, max_value are not correct.";
    }
    return "";
}

string validate_connected_graph(string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    vector<string> tokens = tokenizeProperty(specs);
    if (tokens.size() != 2 || !isVarParam(tokens[0]) || !isVarParam(tokens[1])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) < 1) {
        return ": number of node should be positive.";
    }
    if (var_value(tokens[0]) - 1 > var_value(tokens[1])) {
        return ": number of edges not correct.";
    }
    return "";
}

string validate_weighted_connected_graph(string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    vector<string> tokens = tokenizeProperty(specs);
    if (tokens.size() != 4 || !isVarParam(tokens[0]) || !isVarParam(tokens[1]) || !isVarParam(tokens[2]) || !isVarParam(tokens[3])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) < 1) {
        return ": number of node should be positive.";
    }
    if (var_value(tokens[0]) - 1 > var_value(tokens[1])) {
        return ": number of edges not correct.";
    }
    if (var_value(tokens[2]) > var_value(tokens[3])) {
        return ": min_value, max_value are not correct.";
    }
    return "";
}

string validate_string(string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    vector<string> tokens = tokenizeProperty(specs);
    if (tokens.size() != 5 || !isVarParam(tokens[0]) || !isVarParam(tokens[1])
            || !isVarParam(tokens[2]) || !isVarParam(tokens[3]) || !isCharNotation(tokens[4])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) < 1) {
        return ": number of string should be positive.";
    }
    if (var_value(tokens[1]) < 1) {
        return ": minimum length of string should be positive.";
    }
    if (var_value(tokens[1]) > var_value(tokens[2])) {
        return ": min_length, max_length are not correct.";
    }
    if (var_value(tokens[3]) < 1) {
        return ": maximum total length of string(s) should be positive.";
    }
    if (var_value(tokens[1]) * var_value(tokens[0]) > var_value(tokens[3])) {
        return ": according to the min_length, maximum total length is not correct.";
    }
    return "";
}

string validate_int_matrix(string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    vector<string> tokens = tokenizeProperty(specs);
    if (tokens.size() != 4 || !isVarParam(tokens[0]) || !isVarParam(tokens[1]) || !isVarParam(tokens[2]) || !isVarParam(tokens[3])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) < 1) {
        return ": number of row should be positive.";
    }
    if (var_value(tokens[1]) < 1) {
        return ": number of column should be positive.";
    }
    if (var_value(tokens[2]) > var_value(tokens[3])) {
        return ": min_value, max_value are not correct.";
    }
    return "";
}

string validate_char_matrix(string specs) {
    if (specs.size() < 3 || specs[0] != '[' || specs.back() != ']') {
        return ": formatting is not correct.";
    }
    vector<string> tokens = tokenizeProperty(specs);
    if (tokens.size() != 3 || !isVarParam(tokens[0]) || !isVarParam(tokens[1]) || !isCharNotation(tokens[2])) {
        return ": parameters are not correct.";
    }
    if (var_value(tokens[0]) < 1) {
        return ": number of row should be positive.";
    }
    if (var_value(tokens[1]) < 1) {
        return ": number of column should be positive.";
    }
    return "";
}

pair<bool, string> validate(vector<string> lines) {
    string retMsg = "";
    string error = "script parsing error at line ";
    for (int i = 0; i < lines.size(); ++i) {
        vector<string> scriptTokens = tokenizeScript(lines[i]);
        for (string script : scriptTokens) {
            pair<string, string> type_specs = get_type_specs(script);
            string type = strip(type_specs.first);
            string specs = strip(type_specs.second);

            if (type[0] == '$') {
                retMsg = validate_var(type, specs);
            } else if (type == "int_array") {
                retMsg = validate_int_array(specs);
            } else if (type == "int_pair") {
                retMsg = validate_int_pair(specs);
            } else if (type == "int_permutation") {
                retMsg = validate_int_permutation(specs);
            } else if (type == "tree" || type == "rooted_tree") {
                retMsg = validate_tree(specs);
            } else if (type == "weighted_tree") {
                retMsg = validate_weighted_tree(specs);
            } else if (type == "connected_graph") {
                retMsg = validate_connected_graph(specs);
            } else if (type == "weighted_connected_graph") {
                retMsg = validate_weighted_connected_graph(specs);
            } else if (type == "string") {
                retMsg = validate_string(specs);
            } else if (type == "int_matrix") {
                retMsg = validate_int_matrix(specs);
            } else if (type == "char_matrix") {
                retMsg = validate_char_matrix(specs);
            } else if (type != "line" && type != "space") {
                retMsg = ": command is not recognized.";
            }

            if (retMsg != "") {
                break;
            }
        }

        if (retMsg != "") {
            error += to_string(i + 1) + retMsg;
            break;
        }
    }
    if (retMsg != "") {
        return make_pair(false, error);
    }
    return make_pair(true, "OK");
}

int main() {
    // freopen("input.txt", "r", stdin);
    // freopen("../files/tgenValidation.log", "w", stdout);

    string charset = "";
    for (int i = 0; i < 26; ++i) {
        charset += ('a' + i);
        charset += ('A' + i);
        if (i < 10) {
            charset += '0' + i;
        }
    }
    charset += "$:<->[_]";
    for (char ch : charset) {
        valid_charset.insert(ch);
    }

    vector<string> lines;
    string line;
    while (getline(cin, line)) {
        line = strip(line);
        if (line == "END") {
            break;
        }
        if (line.size() > 0) {
            lines.push_back(line);
        }
    }

    pair<bool, string> validation = validate(lines);

    cout << validation.second;

    return 0;
}