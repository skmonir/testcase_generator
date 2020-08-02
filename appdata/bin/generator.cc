#include <bits/stdc++.h>
#include "testlib.h"

using namespace std;

set<char> valid_charset;
map<string, long long> vars;

/* generator code templates */

long long rnd_wnext(long long minw, long long maxw) {
    return rnd.wnext(minw, maxw, 1);
}

void generate_int_array(int n, long long minw, long long maxw, bool isDistinct, string endWith) {
    vector<long long> a(n);
    if (isDistinct) {
        a = rnd.distinct(n, minw, maxw);
    } else {
        for (int i = 0; i < n; ++i) {
            a[i] = rnd_wnext(minw, maxw);
        }
    }
    for (int i = 0; i < n; ++i) {
        if (i > 0) {
            putchar(endWith == "line" ? '\n' : ' ');
        }
        printf("%lld", a[i]);
    }
}

void generate_int_permutation(int n, int index) {
    vector<int> p = rnd.perm(n, index);
    for (int i = 0; i < n; ++i) {
        if (i > 0) {
            putchar(' ');
        }
        printf("%d", p[i]);
    }
}

void generate_int_pair(int n, long long minw, long long maxw, bool isSecondGreaterEqual) {
    vector<pair<long long, long long>> p(n);
    for (int i = 0; i < n; ++i) {
        p[i].first = rnd_wnext(minw, maxw);
        p[i].second = rnd_wnext(minw, maxw);
        if (isSecondGreaterEqual && p[i].first > p[i].second) {
            swap(p[i].first, p[i].second);
        }
    }
    shuffle(p.begin(), p.end());
    for (int i = 0; i < n; ++i) {
        if (i > 0) {
            putchar('\n');
        }
        printf("%lld %lld", p[i].first, p[i].second);
    }
}

void generate_tree(int n) {
    vector<long long> p(n);
    for (int i = 0; i < n; ++i) {
        if (i > 0) {
            p[i] = rnd_wnext(0, i - 1);
        }
    }

    vector<long long> perm(n);
    for (int i = 0; i < n; ++i) {
        perm[i] = i;
    }
    shuffle(perm.begin() + 1, perm.end());

    vector<pair<long long, long long> > edges;
    for (int i = 1; i < n; i++)
        if (rnd_wnext(0, 1))
            edges.push_back(make_pair(perm[i], perm[p[i]]));
        else
            edges.push_back(make_pair(perm[p[i]], perm[i]));

    shuffle(edges.begin(), edges.end());

    for (int i = 0; i + 1 < n; i++) {
        if (i > 0) {
            putchar('\n');
        }
        printf("%lld %lld", edges[i].first + 1, edges[i].second + 1);
    }
}

void generate_rooted_tree(int n) {
    vector<int> p(n);
    for (int i = 0; i < n; ++i) {
        if (i > 0) {
            p[i] = rnd_wnext(0, i - 1);
        }
    }

    vector<long long> perm(n);
    for (int i = 0; i < n; ++i) {
        perm[i] = i;
    }
    shuffle(perm.begin() + 1, perm.end());

    vector<int> pp(n);
    for (int i = 1; i < n; i++)
        pp[perm[i]] = perm[p[i]];

    for (int i = 1; i < n; i++) {
        printf("%d", pp[i] + 1);
        if (i + 1 < n)
            printf(" ");
    }
}

void generate_weighted_tree(int n, long long minw, long long maxw) {
    vector<long long> p(n);
    for (int i = 0; i < n; ++i) {
        if (i > 0) {
            p[i] = rnd_wnext(0, i - 1);
        }
    }

    vector<long long> perm(n);
    for (int i = 0; i < n; ++i) {
        perm[i] = i;
    }
    shuffle(perm.begin() + 1, perm.end());
    vector<pair<long long, pair<long long, long long>>> edges;

    for (int i = 1; i < n; i++)
        if (rnd_wnext(0, 1))
            edges.push_back(make_pair(rnd_wnext(minw, maxw), make_pair(perm[i], perm[p[i]])));
        else
            edges.push_back(make_pair(rnd_wnext(minw, maxw), make_pair(perm[p[i]], perm[i])));

    shuffle(edges.begin(), edges.end());

    for (int i = 0; i + 1 < n; i++) {
        if (i > 0) {
            putchar('\n');
        }
        printf("%lld %lld %lld", edges[i].second.first + 1, edges[i].second.second + 1, edges[i].first);
    }
}

void generate_connected_graph(int n, int m) {
    vector<long long> p(n);
    for (int i = 0; i < n; ++i) {
        if (i > 0) {
            p[i] = rnd_wnext(0, i - 1);
        }
    }

    vector<long long> perm(n);
    for (int i = 0; i < n; ++i) {
        perm[i] = i;
    }
    shuffle(perm.begin() + 1, perm.end());
    vector<pair<long long, long long> > edges;

    for (int i = 1; i < n; i++)
        if (rnd_wnext(0, 1))
            edges.push_back(make_pair(perm[i], perm[p[i]]));
        else
            edges.push_back(make_pair(perm[p[i]], perm[i]));

    for (int i = n; i <= m; ++i) {
        int u = rnd_wnext(0, n - 1);
        int v = rnd_wnext(0, n - 1);

        edges.push_back(make_pair(u, v));
    }

    shuffle(edges.begin(), edges.end());

    for (int i = 0; i < m; i++) {
        if (i > 0) {
            putchar('\n');
        }
        printf("%lld %lld", edges[i].first + 1, edges[i].second + 1);
    }
}

void generate_weighted_connected_graph(int n, int m, long long minw, long long maxw) {
    vector<long long> p(n);
    for (int i = 0; i < n; ++i) {
        if (i > 0) {
            p[i] = rnd_wnext(0, i - 1);
        }
    }

    vector<long long> perm(n);
    for (int i = 0; i < n; ++i) {
        perm[i] = i;
    }
    shuffle(perm.begin() + 1, perm.end());
    vector<pair<long long, pair<long long, long long>>> edges;

    for (int i = 1; i < n; i++)
        if (rnd_wnext(0, 1))
            edges.push_back(make_pair(rnd_wnext(minw, maxw), make_pair(perm[i], perm[p[i]])));
        else
            edges.push_back(make_pair(rnd_wnext(minw, maxw), make_pair(perm[p[i]], perm[i])));

    for (int i = n; i <= m; ++i) {
        int u = rnd_wnext(0, n - 1);
        int v = rnd_wnext(0, n - 1);

        edges.push_back(make_pair(rnd_wnext(minw, maxw), make_pair(u, v)));
    }

    shuffle(edges.begin(), edges.end());

    for (int i = 0; i < m; i++) {
        if (i > 0) {
            putchar('\n');
        }
        printf("%lld %lld %lld", edges[i].second.first + 1, edges[i].second.second + 1, edges[i].first);
    }
}

void generateString(int numberOfString, int min_length, int max_length, int max_total_len, string notation) {
    string str;
    int len = 0;
    for (int i = 0; i < numberOfString; ++i) {
        int str_to_generate = numberOfString - i - 1;
        int available_len = max_total_len - len;
        available_len = available_len - (str_to_generate * min_length);
        int new_max_len = min(max_length, available_len);
        string cmd = "[" + notation + "]" + "{" + to_string(min_length) + "," + to_string(new_max_len) + "}";
        str = rnd.next(cmd);
        if (i > 0) {
            putchar('\n');
        }
        printf("%s", str.c_str());
        len += (int) str.size();
    }
}

void generate_int_matrix(int row, int column, long long minw, long long maxw) {
    vector<long long> a(column);
    for (int r = 0; r < row; ++r) {
        if (r > 0) {
            putchar('\n');
        }
        for (int i = 0; i < column; ++i) {
            a[i] = rnd_wnext(minw, maxw);
        }
        for (int i = 0; i < column; ++i) {
            if (i > 0) {
                putchar(' ');
            }
            printf("%lld", a[i]);
        }
    }
}

void generate_char_matrix(int row, int column, string notation) {
    string res;
    string cmd = "[" + notation + "]" + "{" + to_string(column) + "," + to_string(column) + "}";
    for (int i = 0; i < row; ++i) {
        if (i > 0) {
            putchar('\n');
        }
        res = rnd.next(cmd);
        printf("%s", res.c_str());
    }
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

long long create_var(string var, long long minw, long long maxw) {
    vars[var] = rnd_wnext(minw, maxw);
    return vars[var];
}

bool var_exists(string var) {
    return vars.count(var) > 0;
}

bool validVarName(string var) {
    if (var.size() < 2 || var[0] != '$' || (var[1] != '_' && !isalpha(var[1]))) {
        return false;
    }
    return true;
}

long long var_value(string var) {
    if (validVarName(var) && var_exists(var)) {
        return vars[var];
    }
    return stol(var);
}

void generateTest(vector<string> lines) {
    for (int i = 0; i < lines.size(); ++i) {
        vector<string> scriptTokens = tokenizeScript(lines[i]);
        for (string script : scriptTokens) {
            pair<string, string> type_specs = get_type_specs(script);
            string type = strip(type_specs.first);
            string specs = strip(type_specs.second);
            vector<string> tokens = tokenizeProperty(specs);

            if (type == "line") {
                printf("\n");
            } else if (type == "space") {
                printf(" ");
            } else if (type[0] == '$') {
                long long minw = var_value(tokens[0]);
                long long maxw = var_value(tokens[1]);
                printf("%lld", create_var(type, minw, maxw));
            } else if (type == "int_array") {
                int size = (int) var_value(tokens[0]);
                long long minw = var_value(tokens[1]);
                long long maxw = var_value(tokens[2]);
                int isDistinct = (int) var_value(tokens[3]);
                string endWith = tokens[4];
                generate_int_array(size, minw, maxw, isDistinct, endWith);
            } else if (type == "int_pair") {
                int size = (int) var_value(tokens[0]);
                long long minw = var_value(tokens[1]);
                long long maxw = var_value(tokens[2]);
                int isSecondGreaterEqual = (int) var_value(tokens[3]);
                generate_int_pair(size, minw, maxw, isSecondGreaterEqual);
            } else if (type == "int_permutation") {
                int size = (int) var_value(tokens[0]);
                int index = var_value(tokens[1]);
                generate_int_permutation(size, index);
            } else if (type == "tree") {
                int size = var_value(tokens[0]);
                generate_tree(size);
            } else if (type == "rooted_tree") {
                int node = var_value(tokens[0]);
                generate_rooted_tree(node);
            } else if (type == "weighted_tree") {
                int size = var_value(tokens[0]);
                long long minw = var_value(tokens[1]);
                long long maxw = var_value(tokens[2]);
                generate_weighted_tree(size, minw, maxw);
            } else if (type == "connected_graph") {
                int node = var_value(tokens[0]);
                int edge = var_value(tokens[1]);
                generate_connected_graph(node, edge);
            } else if (type == "weighted_connected_graph") {
                int node = var_value(tokens[0]);
                int edge = var_value(tokens[1]);
                long long minw = var_value(tokens[2]);
                long long maxw = var_value(tokens[3]);
                generate_weighted_connected_graph(node, edge, minw, maxw);
            } else if (type == "string") {
                int numberOfString = var_value(tokens[0]);
                int min_length = var_value(tokens[1]);
                int max_length = var_value(tokens[2]);
                int max_total_len = var_value(tokens[3]);
                string notation = tokens[4];
                generateString(numberOfString, min_length, max_length, max_total_len, notation);
            } else if (type == "int_matrix") {
                int row = var_value(tokens[0]);
                int column = var_value(tokens[1]);
                long long minw = var_value(tokens[2]);
                long long maxw = var_value(tokens[3]);
                generate_int_matrix(row, column, minw, maxw);
            } else if (type == "char_matrix") {
                int row = var_value(tokens[0]);
                int column = var_value(tokens[1]);
                string notation = tokens[2];
                generate_char_matrix(row, column, notation);
            }
        }
    }
}

int main(int argc, char* argv[]) {
    registerGen(argc, argv, 1);
    // freopen("input.txt", "r", stdin);
    int T = opt<int>(1);

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

    if (T > 0) {
        printf("%d\n", T);
    } else {
        T = 1;
    }
    for (int t = 0; t < T; ++t) {
        if (t > 0) {
            putchar('\n');
        }
        vars.clear();
        generateTest(lines);
    }

    return 0;
}