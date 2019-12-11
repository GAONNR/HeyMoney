<template>
  <v-container fill-height fluid grid-list-xl>
    <v-layout wrap>
      <v-flex sm6 xs12 md6 lg3>
        <material-stats-card
          color="pink"
          icon="mdi-upload"
          title="Debt"
          :value="`${debt}₩`"
          sub-icon="mdi-calendar"
          sub-text="Since 2019.12.12"
        />
      </v-flex>
      <v-flex sm6 xs12 md6 lg3>
        <material-stats-card
          color="blue"
          icon="mdi-download"
          title="Credit"
          :value="`${credit}₩`"
          sub-icon="mdi-calendar"
          sub-text="Since 2019.12.12"
        />
      </v-flex>
      <v-flex md12 lg12>
        <material-card color="pink" title="Debts" text="돈을 제때제때 갚읍시다">
          <v-data-table :headers="headers" :items="debts" hide-actions>
            <template slot="headerCell" slot-scope="{ header }">
              <span class="font-weight-light text-warning text--darken-3" v-text="header.text" />
            </template>
            <template slot="items" slot-scope="{ index, item }">
              <td class="text-xs-right">{{ item.tid }}</td>
              <td>{{ item.name }}</td>
              <td>{{ users[item.creditor_id].name }}</td>
              <td>{{ users[item.debtor_id].name }}</td>
              <td class="text-xs-right">{{ item.price }}</td>
              <td class="text-xs-right">{{ new Date(item.timestamp * 1000).toLocaleString() }}</td>
            </template>
          </v-data-table>
        </material-card>
      </v-flex>
      <v-flex md12 lg12>
        <material-card color="blue" title="Credits" text="돈을 제때제때 갚읍시다">
          <v-data-table :headers="headers" :items="credits" hide-actions>
            <template slot="headerCell" slot-scope="{ header }">
              <span class="font-weight-light text-warning text--darken-3" v-text="header.text" />
            </template>
            <template slot="items" slot-scope="{ index, item }">
              <td class="text-xs-right">{{ item.tid }}</td>
              <td>{{ item.name }}</td>
              <td>{{ users[item.creditor_id].name }}</td>
              <td>{{ users[item.debtor_id].name }}</td>
              <td class="text-xs-right">{{ item.price }}</td>
              <td class="text-xs-right">{{ new Date(item.timestamp * 1000).toLocaleString() }}</td>
            </template>
          </v-data-table>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      username: undefined,
      users: undefined,
      debt: 0,
      credit: 0,
      headers: [
        {
          sortable: false,
          text: '#',
          value: 'tid',
          align: 'right'
        },
        {
          sortable: false,
          text: 'Name',
          value: 'name'
        },
        {
          sortable: false,
          text: 'Creditor ID',
          value: 'creditor_id'
        },
        {
          sortable: false,
          text: 'Debtor ID',
          value: 'debtor_id'
        },
        {
          sortable: false,
          text: 'Price',
          value: 'price',
          align: 'right'
        },
        {
          sortable: true,
          text: 'Timestamp',
          value: 'timestamp',
          align: 'right'
        }
      ],
      credits: [],
      debts: []
    };
  },
  methods: {
    arrayToObject(array) {
      return array.reduce((obj, item) => {
        obj[item.uid] = item;
        return obj;
      });
    },
    getUserInfo() {
      this.$http
        .get(`/api/user?uid=${this.$route.params.uid}`)
        .then(res => {
          this.username = res.data.name;
          this.credit = res.data.credit;
          this.debt = res.data.debt;
        })
        .catch(err => {
          console.log(err);
        });
      this.$http.get('/api/user').then(res => {
        this.users = this.arrayToObject(res.data);
      });
    },
    getCreditTransactions() {
      this.$http
        .get(`/api/transaction?creditor=${this.$route.params.uid}`)
        .then(res => {
          this.credits = res.data;
          console.log(res.data);
        })
        .catch(err => {
          console.log(err);
        });
    },
    getDebtTransactions() {
      this.$http
        .get(`/api/transaction?debtor=${this.$route.params.uid}`)
        .then(res => {
          this.debts = res.data;
          console.log(res.data);
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.getUserInfo();
    this.getCreditTransactions();
    this.getDebtTransactions();
  }
};
</script>
